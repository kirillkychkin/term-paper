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