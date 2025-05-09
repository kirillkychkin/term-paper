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

def read_json_file(filename="tags_keywords.json",):
    with open(filename, 'r', encoding='utf-8') as file:
        data = json.load(file)
    return data

def insert_tag_categories(data):
    tags = []
    for tag in data:
        insert_tag = (tag, )
        tags.append(insert_tag)
    try:
        cnx = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            port=DB_PORT,
            password=DB_PASSWORD,
            database=DB_DATABASE
        )

        cursor = cnx.cursor()
        query_insert = "INSERT INTO tag_categories (name) VALUES (%s)"

        cursor.executemany(query_insert, tags)
        cnx.commit()
        
        results = cursor.fetchall()
        print(results)

    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        if 'cursor' in locals() and cursor is not None:
            cursor.close()
        if 'cnx' in locals() and cnx is not None:
            cnx.close()


def main():
    data = read_json_file()
    insert_tag_categories(data)

if __name__ == "__main__":
    main()
