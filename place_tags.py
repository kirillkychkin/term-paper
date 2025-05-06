import json
import re
from bs4 import BeautifulSoup # type: ignore

# Словарь тегов с ключевыми словами для категоризации
tags_keywords = {
  "machine-learning": [
    "machine learning", "ml", "neural network", "deep learning", "reinforcement learning",
    "scikit-learn", "pytorch", "tensorflow", "model", "classification", "regression",
    "supervised", "unsupervised", "xgboost", "lightgbm"
  ],
  "data-science": [
    "data science", "pandas", "numpy", "jupyter", "notebook", "visualization", "matplotlib",
    "seaborn", "data analysis", "eda", "exploratory data analysis", "data wrangling"
  ],
  "web-development": [
    "web development", "webapp", "web application", "html", "css", "javascript", "frontend",
    "backend", "react", "vue", "angular", "svelte", "nextjs", "nuxt", "tailwind", "sass",
    "typescript", "bootstrap", "responsive design"
  ],
  "frontend": [
    "frontend", "html", "css", "javascript", "react", "vue", "svelte", "nextjs", "nuxt",
    "tailwind", "bootstrap", "sass", "typescript", "ui", "ux"
  ],
  "backend": [
    "backend", "nodejs", "express", "django", "flask", "fastapi", "ruby on rails",
    "api", "server", "rest", "graphql", "routing", "database"
  ],
  "api": [
    "api", "rest", "restful", "graphql", "endpoint", "postman", "swagger", "openapi"
  ],
  "cloud": [
    "cloud", "aws", "gcp", "azure", "lambda", "serverless", "cloud functions", "s3", "ec2",
    "cloud storage", "firebase"
  ],
  "devops": [
    "devops", "docker", "kubernetes", "ci", "cd", "pipeline", "jenkins", "ansible",
    "terraform", "infrastructure", "deployment", "monitoring", "prometheus", "grafana"
  ],
  "mobile": [
    "mobile", "android", "ios", "react native", "flutter", "kotlin", "swift", "mobile app"
  ],
  "game-development": [
    "game", "game dev", "game development", "unity", "unreal", "2d", "3d", "physics",
    "sprites", "game engine", "godot"
  ],
  "ai": [
    "artificial intelligence", "ai", "intelligence", "gpt", "chatbot", "nlp",
    "transformer", "openai", "language model", "bert", "llm"
  ],
  "cli": [
    "cli", "command line", "terminal", "console", "shell", "bash", "zsh", "prompt"
  ],
  "database": [
    "database", "sql", "nosql", "postgresql", "mysql", "mongodb", "sqlite", "query",
    "orm", "prisma", "schema"
  ],
  "security": [
    "security", "encryption", "hashing", "vulnerability", "auth", "authentication",
    "authorization", "jwt", "oauth", "csrf", "xss", "penetration testing"
  ],
  "testing": [
    "test", "testing", "jest", "mocha", "unit test", "integration test", "cypress",
    "pytest", "test coverage", "assertion"
  ],
  "automation": [
    "automation", "bot", "script", "auto", "task runner", "workflow", "rpa", "zapier"
  ],
  "scraping": [
    "scraper", "scraping", "web scraping", "crawler", "beautifulsoup", "requests",
    "selenium", "scrapy", "http client"
  ],
  "design": [
    "design", "ui", "ux", "figma", "sketch", "prototype", "interface", "tailwind",
    "bootstrap", "material ui", "design system"
  ],
  "blockchain": [
    "blockchain", "web3", "ethereum", "solidity", "smart contract", "crypto", "nft",
    "dapp", "metamask"
  ],
  "compiler": [
    "compiler", "interpreter", "parser", "lexer", "syntax", "grammar", "bytecode",
    "ast", "language implementation"
  ],
  "library": [
    "library", "sdk", "toolkit", "framework", "package", "module", "dependency"
  ],
  "plugin": [
    "plugin", "extension", "addon", "integration", "middleware", "hook"
  ],
  "visualization": [
    "visualization", "charts", "graph", "plot", "d3", "plotly", "dash", "bokeh", "chart.js"
  ],
  "networking": [
    "network", "socket", "protocol", "tcp", "udp", "http", "websocket", "client", "server"
  ],
  "robotics": [
    "robot", "robotics", "ros", "sensor", "motion", "servo", "lidar", "path planning"
  ],
  "math": [
    "math", "algebra", "geometry", "calculus", "statistics", "probability", "matrix",
    "equation", "computation", "number theory"
  ],
  "utilities": [
    "utility", "tool", "helper", "cli", "script", "automation", "devtool", "config", "formatter", "linter"
  ],
  "containerization": [
    "container", "docker", "kubernetes", "image", "volume", "containerization"
  ],
  "analytics": [
    "analytics", "tracking", "metrics", "events", "insights", "report", "monitoring", "telemetry"
  ]
}

def clean_text(text: str) -> str:
    if text is None:
        return ""
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

def save_to_file(repos, filename="tagged_repos.json"):
    """Сохранение данных в JSON файл"""
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(repos, f, ensure_ascii=False, indent=2)

def read_json_file(filename="repos_translated_data.json",):
    with open(filename, 'r', encoding='utf-8') as file:
        data = json.load(file)
    return data

def tag_repo(description_text, readme_text):
    """Тегирование репозитория на основе описания и README"""
    # Комбинирование данных для более точного тегирования
    combined_text = description_text + ' ' + readme_text
    repo_tags = dict()
    for tag, keywords in tags_keywords.items():
        # Добавление тега при совпадении любого ключевого слова
        for kw in keywords:
            if kw in combined_text:
                if(tag not in repo_tags):
                    repo_tags[tag] = set()
                else:
                    repo_tags[tag].add(kw)
    repo_tags_listed = dict()                
    # set -> list т.к. set не сохраняется в json
    for tag, keywords in repo_tags.items():
        # удалить пустые списки
        if(len(repo_tags[tag]) != 0):
          repo_tags_listed[tag] = list(keywords)
    
    return repo_tags_listed

def tag_repositories(repositories):
    tagged_repos = []
    counter = 1
    for repo in repositories:
        if(counter > 10):
            continue
        readme_clean = clean_text(repo['readme_text']) 
        description_clean = clean_text(repo['description'])
        repo['tags'] = tag_repo(description_clean, readme_clean) 
        counter += 1
        tagged_repos.append(repo)
    return tagged_repos

def main():
    data = read_json_file()
    data = tag_repositories(data)
    save_to_file(data)
    # langs = get_languages(data)
    # print(langs)

if __name__ == "__main__":
    main()