from pymongo import MongoClient
import urllib.parse
import os

def connect_to_db():
    client = MongoClient(os.getenv(f"mongodb+srv://{urllib.parse.quote(os.getenv('DB_USERNAME'))}:{urllib.parse.quote(os.getenv('DB_PASSWORD'))}@{os.getenv('DB_HOST')}/"))
    return client["cluster0"]