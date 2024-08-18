from pymongo import MongoClient
import certifi
import datetime
from flask import request, jsonify
from bson import ObjectId

mongo_uri = 'mongodb+srv://stalidzanelinda:Galdalete1@snow-api.i2o4l.mongodb.net/?retryWrites=true&w=majority&appName=snow-api'

client = MongoClient(mongo_uri, tlsCAFile=certifi.where())

db = client['snow-api'] 
comments_collection = db['user-comments'] 

def add_user_comment(data):
    comment_data = {
        "user_id": data['user_id'],
        "country1": data['country1'],
        "country2": data['country2'],
        "param2": data['param2'],
        "comment": data['comment'],
        "timestamp": datetime.datetime.now().isoformat()  # Use UTC time for consistency
    }
    
    # Insert the comment into MongoDB
    comments_collection.insert_one(comment_data)
    
    return {"status": "success", "message": "Comment added successfully"}

def get_user_comments():
    # country1 = request.args.get('country1')
    # country2 = request.args.get('country2')
    # param2 = request.args.get('param2')
    
    # # Query MongoDB to find comments matching the criteria
    # query = {
    #     "country1": country1,
    #     "country2": country2,
    #     "param2": param2
    # }
    
    # comments = list(comments_collection.find(query, {"_id": 0}))  # Exclude the MongoDB _id field
    
    cursor = comments_collection.find({}, {"_id": 0}) # Exclude the MongoDB _id field
    comments =  list(d for d in cursor)  

    return jsonify(comments), 200


# try:
#     # List the databases to verify the connection
#     databases = client.list_database_names()
#     print("Connected to MongoDB successfully!")
#     print("Databases:", databases)
# except Exception as e:
#     print("An error occurred:", e)
