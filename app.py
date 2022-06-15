
from flask import Flask
from flask_restful import Api
from flask_restful import Resource, abort
from pymongo import MongoClient
from flask import request
from bson.objectid import ObjectId
import json
from bson import json_util
import os
from dotenv import load_dotenv

app = Flask(__name__)
api = Api(app)

load_dotenv()
mongo_username = os.getenv('MONGO_USERNAME')
mongo_password = os.getenv('MONGO_PASSWORD')
mongo_uri = os.getenv('MONGO_URI')
mongo_db_name = os.getenv('MONGO_DB_NAME')
port = os.getenv('PORT')

client = MongoClient(f'mongodb+srv://{mongo_username}:{mongo_password}@{mongo_uri}/?retryWrites=true&w=majority', 27017)


def get_database():
    return client.lists[mongo_db_name]


class ListView(Resource):
    def post(self):
        json_data = request.get_json()
        db = get_database()
        result = db.insert_one(json_data)
        return {"_id": str(result.inserted_id)}, 200


class ListSingleView(Resource):
    def delete(self, id):
        db = get_database()
        result = db.delete_one({"_id": ObjectId(id)})
        return {"deleted_count": str(result.deleted_count)}, 200


class ListsOfSpaceView(Resource):
    def get(self, space_id):
        user_id = request.headers.get('User-Id')
        db = get_database()
        print(space_id)
        result = db.find({"spaceId": space_id})
        print(result)

        lists = []
        for item in result:
            # breakpoint()
            lists.append(
                json.loads(json_util.dumps(item))
            )

        return lists, 200


api.add_resource(ListsOfSpaceView, "/api/lists/of-space/<space_id>")
api.add_resource(ListView, "/api/lists")
api.add_resource(ListSingleView, "/api/lists/<id>")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=port)
