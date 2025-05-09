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

def get_repository_id(name):
    cnx = mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        port=DB_PORT,
        password=DB_PASSWORD,
        database=DB_DATABASE
    )

    cursor = cnx.cursor(dictionary=True)
    query = "SELECT id from repositories WHERE name = %s"

    cursor.execute(query, name)
    row = cursor.fetchone()
    cursor.close()
    cnx.close()

    return row['id']

def get_lang_id(name):
    cnx = mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        port=DB_PORT,
        password=DB_PASSWORD,
        database=DB_DATABASE
    )

    cursor = cnx.cursor(dictionary=True)
    query = "SELECT id from languages WHERE name = %s"

    cursor.execute(query, name)
    row = cursor.fetchone()
    cursor.close()
    cnx.close()

    return row['id']

def insert_repositories(data):
    repositories_languages = []
    for repo in data:
        name = repo['name']
        repository_id = get_repository_id((name, ))
        for lang in repo['languages_detected']:
            language_id = get_lang_id((lang, ))

            repository = (repository_id, 
                        language_id,
                        )
            repositories_languages.append(repository)

    try:
        cnx = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            port=DB_PORT,
            password=DB_PASSWORD,
            database=DB_DATABASE
        )

        cursor = cnx.cursor()
        query_insert = "INSERT INTO languages_repositories (repository_id, language_id) VALUES (%s, %s)"

        cursor.executemany(query_insert, repositories_languages)
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
    insert_repositories(data)

if __name__ == "__main__":
    main()
