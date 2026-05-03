from pymongo import MongoClient
import certifi
import datetime
import os
from flask import jsonify
from dotenv import load_dotenv

load_dotenv()

mongo_uri = os.getenv('MONGO_URI')
if not mongo_uri:
    raise EnvironmentError("MONGO_URI is not set. Copy .env.example to .env and fill in your credentials.")

client = MongoClient(mongo_uri, tlsCAFile=certifi.where())

db = client['snow-api']
comments_collection = db['user-comments']

def add_user_comment(data):
    comment_data = {
        "user_id": data['user_id'],
        "country1": data['country1'],
        "country2": data['country2'],
        "param": data['param'],
        "comment": data['comment'],
        "timestamp": datetime.datetime.now().isoformat()
    }
    comments_collection.insert_one(comment_data)
    return {"status": "success", "message": "Comment added successfully"}

def get_user_comments():
    cursor = comments_collection.find({}, {"_id": 0})
    comments = list(d for d in cursor)
    return jsonify(comments), 200
