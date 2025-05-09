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

def get_tag_category_id(name):
    cnx = mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        port=DB_PORT,
        password=DB_PASSWORD,
        database=DB_DATABASE
    )

    cursor = cnx.cursor(dictionary=True)
    query = "SELECT id from tag_categories WHERE name = %s"

    cursor.execute(query, name)
    row = cursor.fetchone()
    cursor.close()
    cnx.close()

    return row['id']

def get_tag_id(tuple):
    cnx = mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        port=DB_PORT,
        password=DB_PASSWORD,
        database=DB_DATABASE
    )

    cursor = cnx.cursor(dictionary=True)
    query = "SELECT id from tags WHERE name = %s AND tag_category_id = %s"

    cursor.execute(query, tuple)
    row = cursor.fetchone()
    cursor.close()
    cnx.close()

    return row['id']

def insert_repositories(data):
    repositories_tags = []
    counter = 1
    for repo in data:
        name = repo['name']
        repository_id = get_repository_id((name, ))
        for tag_categ in repo['tags']:
            tag_categ_id = get_tag_category_id((tag_categ, ))
            for tag in repo['tags'][tag_categ]:
                tag_id = get_tag_id((tag, tag_categ_id))
                repository = (repository_id, tag_id)
                repositories_tags.append(repository)
        print("finish for repo #" + str(counter))
        counter += 1
    try:
        cnx = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            port=DB_PORT,
            password=DB_PASSWORD,
            database=DB_DATABASE
        )

        cursor = cnx.cursor()
        query_insert = "INSERT INTO tags_repositories (repository_id, tag_id) VALUES (%s, %s)"

        cursor.executemany(query_insert, repositories_tags)
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
