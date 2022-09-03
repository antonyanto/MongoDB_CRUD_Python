from flask import jsonify, request
from flask_pymongo import pymongo

client = pymongo.MongoClient("mongodb+srv://antony:antony123@cluster0.9u2gmjd.mongodb.net/?retryWrites=true&w=majority")
db = client.get_database('testdb')

user_collection = pymongo.collection.Collection(db, 'users')


def crud_app_api(endpoints):
    @endpoints.route('/hello_world', methods=['GET'])
    def hello_world():
        return '<h1>Hello World</h1>'

    @endpoints.route('read_all_users', methods=['GET'])
    def read_all_user():
        res = {}
        try:
            usersData = user_collection.find({}, projection={"_id": False})
            users = {}
            counter = 1
            for i in usersData:
                users[str(counter)] = i
                counter += 1
            status = {
                "usersData": users,
                "statusCode": "200",
                "statusMessage": "Successfully read all the users in the 'users' collection."
            }
        except Exception as e:
            print("While reading all the users, this error has occurred --> ", e)
            status = {
                "statusCode": "400",
                "statusMessage": "Unable to read all the users in the 'users' collection."
            }
        res = jsonify(status)
        return res

    @endpoints.route('read_user', methods=['GET'])
    def read_user():
        res = {}
        try:
            req_body = request.json
            userData = user_collection.find_one({"userName": req_body["userName"]}, projection={"_id": False})
            status = {
                "userData": userData,
                "statusCode": "200",
                "statusMessage": "Successfully read the user in the 'users' collection."
            }
        except Exception as e:
            print("While reading the user, this error has occurred --> ", e)
            status = {
                "statusCode": "400",
                "statusMessage": "Unable to read the user in the 'users' collection."
            }
        res = jsonify(status)
        return res

    @endpoints.route('/create_user', methods=['POST'])
    def create_user():
        res = {}
        try:
            req_body = request.json
            user_collection.insert_one(req_body)
            status = {
                "statusCode": "200",
                "statusMessage": "Successfully created the new user in the 'users' collection."
            }
        except Exception as e:
            print("While creating the new user, this error has occurred --> ", e)
            status = {
                "statusCode": "400",
                "statusMessage": "Unable to create the new user in the 'users' collection."
            }
        res["status"] = status
        return res

    @endpoints.route('/update_user', methods=['PUT'])
    def update_user():
        res = {}
        try:
            req_body = request.json

            if (req_body["updateProp"] == "subscriptionType"):
                userData = user_collection.update_one(
                    user_collection.find_one({"userName": {"$eq": req_body["userName"]}}),
                    {"$set": {"userSubscriptionType": req_body["userSubscriptionType"]}})
            elif (req_body["updateProp"] == "city"):
                userData = user_collection.update_one(
                    user_collection.find_one({"userName": {"$eq": req_body["userName"]}}),
                    {"$set": {"userCity": req_body["userCity"]}})

            status = {
                "statusCode": "200",
                "statusMessage": "Successfully updated the user in the 'users' collection."
            }
        except Exception as e:
            print("While updating the user, this error has occurred --> ", e)
            status = {
                "statusCode": "400",
                "statusMessage": "Unable to updated the user in the 'users' collection."
            }
        res["status"] = status
        return res

    @endpoints.route('/delete_user', methods=['DELETE'])
    def delete_user():
        res = {}
        try:
            req_body = request.json
            result = user_collection.delete_one({"userName": req_body["userName"]})
            if result.deleted_count == 1:
                status = {
                    "statusCode": "200",
                    "statusMessage": "Successfully deleted the user in the 'users' collection."
                }
            elif result.deleted_count == 0:
                status = {
                    "statusCode": "200",
                    "statusMessage": "No user found with this name in the 'users' collection to delete."
                }
        except Exception as e:
            print("While deleting the user, this error has occurred --> ", e)
            status = {
                "statusCode": "400",
                "statusMessage": "Unable to delete the user in the 'users' collection."
            }
        res["status"] = status
        return res

    return endpoints
