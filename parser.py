# Импорт необходимых библиотек
import requests  # Для выполнения HTTP-запросов к API GitHub
import time  # Для добавления задержки между запросами
import json  # Для работы с JSON-данными
from dotenv import load_dotenv  # Для загрузки переменных окружения из .env файла
import os  # Для работы с операционной системой и переменными окружения

# Загружаем переменные окружения из файла .env
load_dotenv()
# Получаем GitHub токен из переменных окружения для аутентификации
GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')

# Заголовки HTTP-запроса для аутентификации и указания формата ответа
headers = {
    'Authorization': f'token {GITHUB_TOKEN}',  # Токен для доступа к API GitHub
    'Accept': 'application/vnd.github.v3+json'  # Запрашиваем версию 3 API
}

# Поисковый запрос для GitHub:
# Ищем репозитории, содержащие в описании "bachelor thesis" ИЛИ "coursework" и т.д.
search_query = 'bachelor thesis OR coursework OR capstone project'
per_page = 30  # Количество результатов на странице (GitHub позволяет максимум 100)

# Словарь для тегирования репозиториев по ключевым словам
# Ключи - названия тегов, значения - списки ключевых слов для этого тега
tags_keywords = {
    "python": ["python"],
    "unity": ["unity", "c#"],
    "machine learning": ["ml", "machine learning", "deep learning", "neural network"],
    "game development": ["game", "unity", "unreal"],
    "web development": ["web", "website", "frontend", "backend", "fullstack", "django", "flask"],
    "data science": ["data science", "data analysis", "pandas", "numpy"],
}

def get_repos(query, max_pages=2):
    """
    Получает список репозиториев с GitHub по заданному запросу.
    
    Параметры:
        query (str): Поисковый запрос
        max_pages (int): Максимальное количество страниц результатов для получения
        
    Возвращает:
        list: Список репозиториев
    """
    repos = []
    # Проходим по страницам результатов
    for page in range(1, max_pages + 1):
        print(f"Fetching page {page}...")
        # Формируем URL для запроса с параметрами поиска, сортировки и пагинации
        url = f'https://api.github.com/search/repositories?q={query}&sort=stars&order=desc&per_page={per_page}&page={page}'
        # Отправляем GET-запрос с заголовками аутентификации
        response = requests.get(url, headers=headers)
        
        # Проверяем статус ответа
        if response.status_code != 200:
            print(f"Error: {response.status_code}")
            break
        
        # Парсим JSON-ответ
        data = response.json()
        # Добавляем найденные репозитории в общий список
        repos.extend(data.get('items', []))
        # Делаем паузу, чтобы не превысить лимит запросов к API
        time.sleep(2)
    
    return repos

def tag_repo(repo):
    """
    Добавляет теги к репозиторию на основе его описания и тем.
    
    Параметры:
        repo (dict): Данные репозитория
        
    Возвращает:
        list: Список тегов для репозитория
    """
    # Собираем весь текст для анализа (описание + темы)
    text = (repo.get('description') or '').lower() + ' ' + ' '.join(repo.get('topics', []))
    repo_tags = []
    
    # Проверяем каждую категорию тегов
    for tag, keywords in tags_keywords.items():
        # Если хотя бы одно ключевое слово найдено в тексте
        if any(kw in text for kw in keywords):
            repo_tags.append(tag)  # Добавляем соответствующий тег
    
    return repo_tags

def save_to_file(repos, filename="repos_data.json"):
    """
    Сохраняет данные о репозиториях в JSON-файл.
    
    Параметры:
        repos (list): Список репозиториев для сохранения
        filename (str): Имя файла для сохранения
    """
    with open(filename, 'w', encoding='utf-8') as f:
        # Записываем данные с отступами для удобного чтения
        json.dump(repos, f, ensure_ascii=False, indent=2)

def main():
    """
    Основная функция: выполняет поиск, тегирование и сохранение репозиториев.
    """
    # Получаем репозитории (ищем 5 страниц результатов)
    repos = get_repos(search_query, max_pages=5)
    print(f"Fetched {len(repos)} repositories")

    # Добавляем теги к каждому репозиторию
    tagged_repos = []
    for repo in repos:
        tags = tag_repo(repo)
        # Формируем структуру данных для сохранения
        tagged_repos.append({
            "name": repo.get('full_name'),  # Полное имя репозитория
            "url": repo.get('html_url'),  # Ссылка на репозиторий
            "description": repo.get('description'),  # Описание
            "language": repo.get('language'),  # Основной язык программирования
            "tags": tags  # Наши теги
        })

    # Сохраняем результаты в файл
    save_to_file(tagged_repos)
    print("Saved tagged repositories to repos_data.json")

# Точка входа в программу
if __name__ == "__main__":
    main()