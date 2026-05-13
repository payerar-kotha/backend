from pymongo import MongoClient
import urllib.parse
import os

def connect_to_db():
    client = MongoClient(f"mongodb+srv://{urllib.parse.quote_plus(os.getenv('DB_USERNAME'))}:{urllib.parse.quote_plus(os.getenv('DB_PASSWORD'))}@{os.getenv('DB_HOST')}/")
    return client["chat-app"]