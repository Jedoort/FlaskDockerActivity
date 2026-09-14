from pymongo import MongoClient
import os
from bson import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash

def init_db():
    uri = os.environ.get('MONGO_URI')
    client = MongoClient(uri)
    return client["FlaskApp-Docker"]

def get_items(db):
    return [ {"_id": str(doc['_id']), "name": doc['name']} for doc in db.items.find() ]

def add_item(db, data):
    result = db.items.insert_one({"name": data['name']})
    return {"inserted_id": str(result.inserted_id)}

def delete_item(db, item_id):
    db.items.delete_one({'_id': ObjectId(item_id)})
    return {"status": "deleted"}

def register_user(db, username, password):
    hashed_pwd = generate_password_hash(password)
    db.users.insert_one({"username": username, "password": hashed_pwd})
    return {"status": "user registered"}

def login_user(db, username, password):
    user = db.users.find_one({"username": username})
    if user and check_password_hash(user["password"], password):
        return {"status": "logged in"}
    return {"error": "invalid credentials"}