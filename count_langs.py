import json

def save_to_file(repos, filename="languages_list.json"):
    """Сохранение данных в JSON файл"""
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(repos, f, ensure_ascii=False, indent=2)

def read_json_file(filename="repos_data.json",):
    with open(filename, 'r', encoding='utf-8') as file:
        data = json.load(file)
    return data

def count_langs(data):
    programming_languages = set()
    counter = 1
    for repo in data:
        repo_langs = repo['languages_detected']
        for lang in repo_langs:
            programming_languages.add(lang)
        print("repo " + str(counter) + " was scanned")
        counter += 1

    data = []
    for lang in programming_languages:
        item = dict()
        item['name'] = lang
        data.append(item)
    return data

def main():
    data = read_json_file()
    data = count_langs(data)
    save_to_file(data)
    print(data)
    # langs = get_languages(data)
    # print(langs)

if __name__ == "__main__":
    main()