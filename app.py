import os
from flask import Flask, Response, request, jsonify, make_response
from dotenv import load_dotenv
from pymongo import MongoClient
from bson.json_util import dumps
from bson.objectid import ObjectId

load_dotenv()

app = Flask(__name__)
mongo_db_url = ("mongodb+srv://admin:49cpmq9oY8UMLiJN@cluster0.lnhqubz.mongodb.net/test")

client = MongoClient(mongo_db_url)
db = client['test']
print(mongo_db_url)

@app.get("/api/smoketests")
def get_smoketests():
    sensor_id = request.args.get('sensor_id')
    filter = {} if sensor_id is None else {"sensor_id": sensor_id}
    smoketests = list(db.smoketests.find(filter))
    print(smoketests)

    response = Response(
        response=dumps(smoketests), status=200,  mimetype="application/json")
    return response

@app.post("/api/smoketests")
def add_sensor():
    _json = request.json
    db.smoketests.insert_one(_json)

    resp = jsonify({"message": "Sensor added successfully"})
    resp.status_code = 200
    return resp


@app.delete("/api/smoketests/<id>")
def delete_sensor(id):
    db.smoketests.delete_one({'_id': ObjectId(id)})

    resp = jsonify({"message": "Sensor deleted successfully"})
    resp.status_code = 200
    return resp 

@app.put("/api/smoketests/<id>")
def update_sensor(id):
    _json = request.json
    db.smoketests.update_one({'_id': ObjectId(id)}, {"$set": _json})

    resp = jsonify({"message": "Sensor updated successfully"})
    resp.status_code = 200
    return resp

@app.errorhandler(400)
def handle_400_error(error):
    return make_response(jsonify({"errorCode": error.code, 
                                  "errorDescription": "Bad request!",
                                  "errorDetailedDescription": error.description,
                                  "errorName": error.name}), 400)

@app.errorhandler(404)
def handle_404_error(error):
        return make_response(jsonify({"errorCode": error.code, 
                                  "errorDescription": "Resource not found!",
                                  "errorDetailedDescription": error.description,
                                  "errorName": error.name}), 404)

@app.errorhandler(500)
def handle_500_error(error):
        return make_response(jsonify({"errorCode": error.code, 
                                  "errorDescription": "Internal Server Error",
                                  "errorDetailedDescription": error.description,
                                  "errorName": error.name}), 500) 