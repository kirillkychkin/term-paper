import fasttext
import json
import re
import argostranslate.package
import argostranslate.translate
from bs4 import BeautifulSoup
installed_languages = argostranslate.translate.load_installed_languages()

model = fasttext.load_model("lid.176.bin")

import re
from bs4 import BeautifulSoup

def save_to_file(repos, filename="repos_translated_data.json"):
    """Сохранение данных в JSON файл"""
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(repos, f, ensure_ascii=False, indent=2)

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

def translate_text(text, from_code, to_code='en'):
    from_lang = next((l for l in installed_languages if l.code == from_code), None)
    to_lang = next((l for l in installed_languages if l.code == to_code), None)

    if from_lang and to_lang:
        translation = from_lang.get_translation(to_lang)
        return translation.translate(text)
    return text  # fallback: return original if no translation available

def predict_lang(text):
    pred = model.predict(text)
    label = pred[0][0].replace("__label__", "")
    confidence = pred[1][0]
    return label, confidence

def read_json_file(filename="repos_data.json"):
    with open(filename, 'r') as file:
        data = json.load(file)
    return data

def translate_readme(data):
    translated_readmes = []
    for repo in data:
        readme_text_plain = repo['readme_text'].replace('\n', ' ')
        if(readme_text_plain == ""):
            continue
        readme_clean = clean_readme(readme_text_plain)
        readme_lang, confidence = predict_lang(readme_clean)
        entry = {}
        if(readme_lang != "en"):
            try:
                entry["readme"] = translate_text(repo['readme_text'], from_code=readme_lang)
                translated_readmes.append(entry)
            except Exception as e:
                print(f"Translation error: {e}")
    return translated_readmes

def main():
    data = read_json_file()
    data = translate_readme(data)
    save_to_file(data)

if __name__ == "__main__":
    main()
