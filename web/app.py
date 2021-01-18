from flask import Flask, jsonify, request
from flask_restful import Api, Resource
from pymongo import MongoClient
import bcrypt


app = Flask(__name__)
api = Api(app)
client = MongoClient("mongodb://db:27017")
db = client.SimilarityDB
users = db['Users']

def user_exists(username):
    if users.find({
        "Username": username
    }).count() == 0:
        return False
    return True

class Register(Resource):
    def post(self):
        posted_data = request.get_json()
        username = posted_data["username"]
        password = posted_data["password"]
        if user_exists(username):
            ret_json = {
                "status": 301,
                "msg": "Invalid Username"
            }
            return jsonify(ret_json)

        hashed_pw = bcrypt.hashpw(password.encode('utf8'), bcrypt.gensalt())
        users.insert_one({
            "Username": username,
            "Password": hashed_pw,
            "Tokens": 6
        })

        ret_json = {
            "status": 200,
            "msg": "You've successfully signed up to the API"
        }
        return jsonify(ret_json)
