import fasttext # type: ignore
import json
import re
import argostranslate.translate # type: ignore
from bs4 import BeautifulSoup # type: ignore
installed_languages = argostranslate.translate.get_installed_languages()

model = fasttext.load_model("lid.176.bin")

def save_to_file(repos, filename="repos_translated_data.json"):
    """Сохранение данных в JSON файл"""
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(repos, f, ensure_ascii=False, indent=2)

def clean_readme(text: str) -> str:
    # Remove fenced code blocks ```...``` with language or without
    text = re.sub(r'```[\s\S]*?```', '', text)

    # Remove indented code blocks (lines starting with 4+ spaces or a tab)
    text = re.sub(r'(?m)^( {4}|\t).+', '', text)

    # Remove inline code (e.g. `command`)
    text = re.sub(r'`[^`]+`', '', text)

    # Remove markdown images and links: ![alt](url), [text](url)
    text = re.sub(r'!\[[^\]]*\]\([^)]*\)', '', text)
    text = re.sub(r'\[[^\]]*\]\([^)]*\)', '', text)

    # Remove plain URLs
    text = re.sub(r'https?://\S+|www\.\S+', '', text)

    # Remove HTML tags
    text = BeautifulSoup(text, 'html.parser').get_text()

    # Remove extra whitespace
    text = re.sub(r'\s+', ' ', text).strip()

    return text

def translate_text(text, from_code, to_code='en'):
    from_lang = next((l for l in installed_languages if l.code == from_code), None)
    to_lang = next((l for l in installed_languages if l.code == to_code), None)

    if from_lang and to_lang:
        translation = from_lang.get_translation(to_lang)
        # return translation.translate(text)
    else:
        # print(from_code, to_code)
        return "translation error"
    # return text  # fallback: return original if no translation available
    # Split markdown into translatable parts (skip code blocks)
    parts = []
    code_block = False
    buffer = []

    for line in text.splitlines(keepends=True):
        if line.strip().startswith("```"):
            code_block = not code_block
            parts.append("".join(buffer))
            buffer = [line]
        elif code_block:
            buffer.append(line)
        else:
            buffer.append(line)

    parts.append("".join(buffer))

    # Translate only non-code blocks
    translated_parts = []
    is_code = False
    for part in parts:
        if part.strip().startswith("```"):
            is_code = not is_code
            translated_parts.append(part)
        elif is_code:
            translated_parts.append(part)
        else:
            translation = from_lang.get_translation(to_lang)
            translated_parts.append(translation.translate(part))

    return "".join(translated_parts)

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
    counter = 0
    for repo in data:
        readme_text_plain = repo['readme_text'].replace('\n', ' ')
        if(readme_text_plain == ""):
            continue
        readme_clean = clean_readme(readme_text_plain)
        readme_lang, confidence = predict_lang(readme_clean)
        entry = {}
        if(readme_lang != "en"):
            try:
                entry["readme"] = translate_text(repo['readme_text'], 
                from_code=readme_lang)
                entry["readme_before"] = repo['readme_text']
                counter += 1
                print("end translation procedure # " + str(counter))
                translated_readmes.append(entry)
            except Exception as e:
                print(f"Translation error: {e}")
    return translated_readmes

def get_languages(data):
    languages = set()
    for repo in data:
        readme_text_plain = repo['readme_text'].replace('\n', ' ')
        if(readme_text_plain == ""):
            continue
        readme_clean = clean_readme(readme_text_plain)
        readme_lang, confidence = predict_lang(readme_clean)
        if(readme_lang != "en"):
            languages.add(readme_lang)
    return languages

def main():
    data = read_json_file()
    data = translate_readme(data)
    save_to_file(data)
    # langs = get_languages(data)
    # print(langs)

if __name__ == "__main__":
    main()
