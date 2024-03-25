from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from dotenv import load_dotenv
import os

load_dotenv()

uri = os.getenv("db_string")
key = os.getenv("key")

try:
    client = MongoClient(uri, server_api=ServerApi('1'))
except Exception as e:
    print(e)




