import pymongo
from dotenv import load_dotenv
from os import environ

# Load environment variables from .env file
load_dotenv()

# Global variable to hold the database client instance
db_client = None
db_name = environ.get("DB_NAME")


def init_db(app):
    client = pymongo.MongoClient(environ.get("MONGODB_URI"))
    app.config["DB_CLIENT"] = client
    app.config["DB_NAME"] = db_name
    global db_client
    db_client = client


def get_db():
    if db_client is None:
        raise Exception(
            "Database client is not initialized. Call init_db(uri, db_name) first."
        )
    return db_client[db_name]


def get_collection(collection_name):
    db = get_db()
    return db[collection_name]
