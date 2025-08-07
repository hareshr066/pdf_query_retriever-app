import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")
DB_NAME = os.getenv("DB_NAME")
COLLECTION_NAME = os.getenv("COLLECTION_NAME")

client = MongoClient(MONGO_URI)
db = client[DB_NAME]
collection = db[COLLECTION_NAME]

def insert_pdf_content(filename, content):
    document = {
        "filename": filename,
        "content": content
    }
    result = collection.insert_one(document)
    return result.inserted_id

def fetch_all_documents():
    return list(collection.find({}, {"_id": 0}))
