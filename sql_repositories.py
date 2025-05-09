from dotenv import load_dotenv
import mysql.connector
import json
import os
load_dotenv()
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_HOST = os.getenv('DB_HOST')
DB_USER = os.getenv('DB_USER')
DB_PORT = os.getenv('DB_PORT')
DB_DATABASE = os.getenv('DB_DATABASE')

def read_json_file(filename="tagged_repos.json",):
    with open(filename, 'r', encoding='utf-8') as file:
        data = json.load(file)
    return data

def insert_repositories(data):
    repositories = []
    for repo in data:
        translated_readme_text = None
        readme_russian = None
        readme_lang = None
        readme = None

        name = ""
        url = ""
        if 'name' in repo:
            name = repo['name']
        if 'url' in repo:
            url = repo['url']

        if 'readme_text' in repo:
            readme = repo['readme_text']
        if 'readme_lang' in repo:
            readme_lang = repo['readme_lang']
            if(repo['readme_lang'] != 'en'):
                translated_readme_text = repo['translated_readme_text']
            if(repo['readme_lang'] != 'ru'):
                readme_russian = repo['readme_russian']

        translated_description = None
        description_russian = None
        description_lang = None
        description = None
        
        if 'description' in repo:
            description = repo['description']

        if 'description_lang' in repo:
            description_lang = repo['description_lang']
            if(repo['description_lang'] != 'en'):
                translated_description = repo['translated_description']
            if(repo['description_lang'] != 'ru'):
                description_russian = repo['description_russian']

        repository = (name, 
                      url,
                      readme,
                      readme_lang,
                      translated_readme_text,
                      readme_russian,
                      description,
                      description_lang,
                      translated_description,
                      description_russian
                    )
        repositories.append(repository)
        # print(repository)

    try:
        cnx = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            port=DB_PORT,
            password=DB_PASSWORD,
            database=DB_DATABASE
        )

        cursor = cnx.cursor()
        query_insert = "INSERT INTO repositories (name, url, readme_text, readme_lang, translated_readme_text, readme_russian, description, description_lang, translated_description, description_russian) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"

        cursor.executemany(query_insert, repositories)
        cnx.commit()

    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        if 'cursor' in locals() and cursor is not None:
            cursor.close()
        if 'cnx' in locals() and cnx is not None:
            cnx.close()


def main():
    data = read_json_file()
    insert_repositories(data[:1000])

if __name__ == "__main__":
    main()
