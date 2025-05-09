from dotenv import load_dotenv
import mysql.connector
import os
load_dotenv()
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_HOST = os.getenv('DB_HOST')
DB_USER = os.getenv('DB_USER')
DB_PORT = os.getenv('DB_PORT')
DB_DATABASE = os.getenv('DB_DATABASE')

try:
    cnx = mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        port=DB_PORT,
        password=DB_PASSWORD,
        database=DB_DATABASE
    )

    cursor = cnx.cursor()
    query = "SELECT * FROM tag_categories"
    cursor.execute(query)
    
    results = cursor.fetchall()
    print(results)

except mysql.connector.Error as err:
    print(f"Error: {err}")
finally:
    if 'cursor' in locals() and cursor is not None:
        cursor.close()
    if 'cnx' in locals() and cnx is not None:
        cnx.close()