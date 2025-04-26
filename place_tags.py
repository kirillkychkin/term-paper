# Словарь тегов с ключевыми словами для категоризации
tags_keywords = {
    "python": ["python"],
    "unity": ["unity", "c#"],
    "machine learning": ["ml", "machine learning", "deep learning", "neural network"],
    "game development": ["game", "unity", "unreal"],
    "web development": ["web", "website", "frontend", "backend", "fullstack", "django", "flask"],
    "data science": ["data science", "data analysis", "pandas", "numpy"],
}

def tag_repo(repo, readme_text):
    """Тегирование репозитория на основе описания и README"""
    print(f"Tagging repository {repo.get('full_name')}...")
    # Комбинирование данных для более точного тегирования
    combined_text = (repo.get('description') or '').lower() + ' ' + readme_text
    repo_tags = []
    for tag, keywords in tags_keywords.items():
        # Добавление тега при совпадении любого ключевого слова
        if any(kw in combined_text for kw in keywords):
            repo_tags.append(tag)
    print(f"Tags found: {repo_tags}")
    return repo_tags