import fasttext
import json
import re
from bs4 import BeautifulSoup

model = fasttext.load_model("lid.176.bin")

import re
from bs4 import BeautifulSoup

def clean_readme(text: str) -> str:
    # Remove fenced code blocks ```...``` (multiline)
    text = re.sub(r'```[\s\S]*?```', '', text)
    
    # Remove inline code `...`
    text = re.sub(r'`[^`]+`', '', text)
    
    # Remove Markdown image and link syntax: ![alt](url) and [text](url)
    text = re.sub(r'!\[[^\]]*\]\([^)]*\)', '', text)
    text = re.sub(r'\[[^\]]*\]\([^)]*\)', '', text)

    # Remove raw URLs
    text = re.sub(r'https?://\S+|www\.\S+', '', text)

    # Remove HTML tags using BeautifulSoup
    text = BeautifulSoup(text, 'html.parser').get_text()

    # Remove excess whitespace
    text = re.sub(r'\s+', ' ', text).strip()

    return text


def predict_lang(text):
    pred = model.predict(text)
    label = pred[0][0].replace("__label__", "")
    confidence = pred[1][0]
    return label, confidence

def read_json_file(filename="repos_data.json"):
    with open(filename, 'r') as file:
        data = json.load(file)
    return data

def calculate_readme(data):
    eng = 0
    not_eng = 0
    no_readme = 0

    dataset_length = len(data)
    overall_confidence = 0

    for repo in data:
        readme_text_plain = repo['readme_text'].replace('\n', ' ')
        if(readme_text_plain == ""):
            no_readme += 1
            # если нет readme - убавим длину, чтобы не нарушались подсчеты
            dataset_length -= 1
            continue
        readme_clean = clean_readme(readme_text_plain)
        readme_lang, confidence = predict_lang(readme_clean)
        overall_confidence += confidence
        # if(confidence < 0.6):
        #     print("small confidence detected!: \n" + readme_clean + "\n confidence: " + str(confidence) + "\n predicted_lang: " + str(readme_lang))
        if(readme_lang == "en"):
            eng += 1
        else:
            not_eng += 1
    avg_conf = overall_confidence / dataset_length
    return eng, not_eng, no_readme, avg_conf

def main():
    data = read_json_file()
    eng, not_eng, no_readme, avg_conf = calculate_readme(data)
    print("total eng: " + str(eng) + "\n total not eng " + str(not_eng) + "\n no readme: " + str(no_readme) + "\n avg confidence: " + str(avg_conf))
    calculate_readme(data)

if __name__ == "__main__":
    main()
