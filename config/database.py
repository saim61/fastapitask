import sys

from pymongo import MongoClient

MONGO_URI = "mongodb://mongo:27017/"
client = MongoClient(MONGO_URI)

if "pytest" in sys.modules:
    users_db = client.test_users_db
    users_collection_name = users_db["test_users_collection"]

    candidates_db = client.test_candidates_db
    candidates_collection_name = candidates_db["test_candidates_collection"]
else:
    users_db = client.users_db
    users_collection_name = users_db["users_collection"]

    candidates_db = client.candidates_db
    candidates_collection_name = candidates_db["candidates_collection"]
