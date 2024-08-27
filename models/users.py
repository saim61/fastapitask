from bson import ObjectId
from pydantic import BaseModel
from config.database import users_collection_name

class User(BaseModel):
    id: str
    username: str
    password: str
    name: str

class SignUpUserRequest(BaseModel):
    username: str
    password: str
    name: str

class LoginUserRequest(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str
    message: str

def user_serializer(user: User) -> dict:
    return {
        "id": str(user["_id"]),
        "name": user["name"],
        "username": user["username"],
        "password": user["password"],
    }

def users_serialize(users) -> list:
    return [user_serializer(user) for user in users]

def find_user_by_id(_id: str) -> dict:
    the_user = users_collection_name.find_one({"_id": ObjectId(_id)})
    if the_user is None:
        return {}
    return user_serializer(the_user)

def find_user_by_username(username: str) -> dict:
    the_user = users_collection_name.find_one({"username": username})
    if the_user is None:
        return {}

    return user_serializer(the_user)

def insert_user(user: SignUpUserRequest):
    return users_collection_name.insert_one(dict(user))

def get_all_users():
    return users_serialize(users_collection_name.find())

def delete_all_users():
    users_collection_name.drop()