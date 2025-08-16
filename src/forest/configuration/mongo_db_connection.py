import sys
from src.forest.exception import ForestException
import os
from src.forest.constant.database import DATABASE_NAME
import pymongo
import certifi
from dotenv import load_dotenv

load_dotenv()

ca = certifi.where()

class MongoDBClient:
    client = None

    def __init__(self, database_name=DATABASE_NAME) -> None:
        try:
            if MongoDBClient.client is None:
                mongo_db_url = os.getenv("MONGODB_URL")
                if mongo_db_url is None:
                    raise Exception("Environment key MONGODB_URL is not set.")
                
                # Use TLS parameters for PyMongo 4.x
                MongoDBClient.client = pymongo.MongoClient(
                    mongo_db_url,
                    tls=True,
                    tlsCAFile=certifi.where(),
                    tlsAllowInvalidCertificates=True,
                    serverSelectionTimeoutMS=120000,
                    connectTimeoutMS=120000,
                    socketTimeoutMS=120000
                )
                
            self.client = MongoDBClient.client
            self.database = self.client[database_name]
            self.database_name = database_name
        except Exception as e:
            raise ForestException(e, sys)
