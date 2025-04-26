import requests
import time
import json
import base64
import os
from dotenv import load_dotenv

# Безопасная загрузка токена из .env файла
load_dotenv()
GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')

# Headers для аутентификации с повышенным лимитом запросов (5000/час вместо 60)
headers = {
    'Authorization': f'token {GITHUB_TOKEN}',
    'Accept': 'application/vnd.github.v3+json'  # Версия API с поддержкой topics и languages
}

def requests_get(url, headers=None, max_retries=3):
    """Безопасный запрос с обработкой превышения лимита и повторами"""
    attempt = 0
    while attempt < max_retries:
        response = requests.get(url, headers=headers)
        
        if response.status_code == 403:
            # Проверяем, не превышен ли лимит запросов
            if 'X-RateLimit-Reset' in response.headers:
                reset_time = int(response.headers.get('X-RateLimit-Reset', time.time() + 60))
                wait_seconds = reset_time - int(time.time()) + 5  # Небольшой запас
                print(f"Rate limit exceeded. Sleeping for {wait_seconds} seconds...")
                time.sleep(wait_seconds)
                continue  # После ожидания повторяем запрос
            else:
                print("403 Forbidden received without RateLimit headers. Waiting 60 seconds...")
                time.sleep(60)
                continue

        if response.status_code in [500, 502, 503, 504]:
            # Ошибки сервера, повторяем попытку
            print(f"Server error {response.status_code}. Retrying in 10 seconds...")
            time.sleep(10)
            attempt += 1
            continue

        return response  # Всё хорошо, возвращаем ответ

    print(f"Failed to fetch {url} after {max_retries} attempts.")
    return None

# Поисковый запрос
search_query = 'bachelor thesis OR coursework OR capstone project'
per_page = 30  # Оптимальное значение для баланса скорости и количества данных

def get_repos(query):
    repos = []
    page = 1
    while True:
        print(f"Fetching page {page}...")
        url = f'https://api.github.com/search/repositories?q={query}&sort=stars&order=desc&per_page={per_page}&page={page}'
        response = requests_get(url, headers=headers)

        if response is None:
            print("Giving up fetching repositories.")
            break
        data = response.json()
        items = data.get('items', [])

        if not items:
            print("No more repositories found. Stopping.")
            break

        repos.extend(items)
        print(f"Fetched {len(items)} repositories on page {page}")

        page += 1
        time.sleep(2)

    return repos

def get_readme(owner, repo_name):
    print(f"Fetching README for {owner}/{repo_name}...")
    url = f'https://api.github.com/repos/{owner}/{repo_name}/readme'
    response = requests_get(url, headers=headers)

    if response and response.status_code == 200:
        content = base64.b64decode(response.json()['content']).decode('utf-8', errors='ignore')
        print(f"Successfully fetched README for {owner}/{repo_name}")
        return content.lower()
    else:
        print(f"Failed to fetch README for {owner}/{repo_name}")
        return ""

def get_languages(owner, repo_name):
    print(f"Fetching languages for {owner}/{repo_name}...")
    url = f'https://api.github.com/repos/{owner}/{repo_name}/languages'
    response = requests_get(url, headers=headers)

    if response and response.status_code == 200:
        print(f"Successfully fetched languages for {owner}/{repo_name}")
        return response.json()
    else:
        print(f"Failed to fetch languages for {owner}/{repo_name}")
        return {}


def save_to_file(repos, filename="repos_data.json"):
    """Сохранение данных в JSON файл"""
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(repos, f, ensure_ascii=False, indent=2)

def main():
    repos = get_repos(search_query)
    print(f"Fetched {len(repos)} repositories")

    res_repos = []
    for repo in repos:
        # Извлечение владельца и имени репозитория из структуры ответа
        owner, repo_name = repo['owner']['login'], repo['name']

        readme_text = get_readme(owner, repo_name)
        languages_data = get_languages(owner, repo_name)
        # Сортировка языков по количеству кода (убывание)
        main_languages = sorted(languages_data.items(), key=lambda item: item[1], reverse=True)
        main_languages = [lang for lang, _ in main_languages]

        res_repos.append({
            "name": repo.get('full_name'),
            "url": repo.get('html_url'),
            "description": repo.get('description'),
            "languages_detected": main_languages,
            "readme_text": readme_text,
            "repo": repo
        })

        time.sleep(1)  # Вежливая задержка между запросами

    save_to_file(res_repos)
    print("Saved repositories to repos_data.json")

if __name__ == "__main__":
    main()