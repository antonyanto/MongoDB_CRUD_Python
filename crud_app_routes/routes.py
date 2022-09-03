from flask import jsonify, request
from flask_pymongo import pymongo

client = pymongo.MongoClient("mongodb+srv://antony:antony123@cluster0.9u2gmjd.mongodb.net/?retryWrites=true&w=majority")
db = client.get_database('testdb')
print("Successfully Connected to the Database...")

user_collection = pymongo.collection.Collection(db, 'users')
print("Successfully Retrieved 'Users' Collection...")


def crud_app_api(endpoints):
    @endpoints.route('/hello_world', methods=['GET'])
    def hello_world():
        return '<h1>Hello World</h1>'

    return endpoints
