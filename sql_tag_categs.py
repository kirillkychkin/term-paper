from dotenv import load_dotenv
import mysql.connector
import os
load_dotenv()
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_HOST = os.getenv('DB_HOST')
DB_USER = os.getenv('DB_USER')
DB_PORT = os.getenv('DB_PORT')
DB_DATABASE = os.getenv('DB_DATABASE')

mydb = mysql.connector.connect(
  host=DB_HOST,
  user=DB_USER,
  port=DB_PORT,
  password=DB_PASSWORD,
  database=DB_DATABASE
)

print(mydb)
mydb.close()