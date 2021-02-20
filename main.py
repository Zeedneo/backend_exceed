from flask import Flask, request, Response, jsonify
from flask_pymongo import PyMongo
import json

from flask_cors import CORS, cross_origin

app = Flask(__name__)
cors = CORS(app, resources={r"/": {"origins": "*"}})
app.config['MONGO_URI'] = 'mongodb://exceed_group13:zb924yhy@158.108.182.0:2255/exceed_group13'
mongo = PyMongo(app)


@app.route('/test', methods=['GET'])
@cross_origin()
def hello():
    return {'res': 'hello world'}


@app.route('/find_all', methods=['GET'])
@cross_origin()
def find():
    myCollection = mongo.db.test
    user_name = request.args.get("robotNo")
    if user_name != None:
        flit = {"robotNo": int(user_name)}
        query = myCollection.find(flit)
    else:
        query = myCollection.find()
    output = []
    for ele in query:
        output.append({
            "robotNo": ele["robotNo"],
            "status": ele["status"],
            "sensor1": ele["sensor1"],
            "sensor2": ele["sensor2"],
            "sensor3": ele["sensor3"]
        })
    return {"result": output}


@app.route('/create', methods=['POST'])
@cross_origin()
def from_robot():
    myCollection = mongo.db.test
    data = request.json
    myInsert = {
        "robotNo": data["robotNo"],
        "status": data["status"],
        "sensor1": data["sensor1"],
        "sensor2": data["sensor2"],
        "sensor3": data["sensor3"]
    }
    myCollection.insert_one(myInsert)
    return {"result": "Create succesfully"}


@app.route('/find_all_patient', methods=['GET'])
@cross_origin()
def find_patient():
    myCollection = mongo.db.patient
    myCollection2 = mongo.db.info_patient
    myName = request.args.get("patient_room")
    if myName != None:
        flit = {"patient_room": myName}
        # flit2 = {"RoomNo": myName}
        query = myCollection.find(flit)
        # query2 = myCollection2.find(flit2)
    else:
        query = myCollection.find()
    output = []
    for ele in query:
        tmp = {}
        flit2 = {"RoomNo": ele["patient_room"]}
        query2 = myCollection2.find(flit2)
        for i in query2:
            tmp["Name"] = i["Name"]
            tmp["Gender"] = i["Gender"]
            tmp["BirthDate"] = i["BirthDate"]
            tmp["Addres"] = i["Addres"]
            tmp["Zip_Code"] = i["Zip_Code"]
            tmp["Doctor"] = i["Doctor"]
            tmp["Height"] = i["Height"]
            tmp["Weight"] = i["Weight"]
            tmp["Medical"] = i["Medical"]
            tmp["Allergic_drugs"] = i["Allergic_drugs"]

        output.append({
            "patient_room": ele["patient_room"],
            "patient": tmp
        })
    return Response(json.dumps(output), mimetype='application/json')


@app.route('/find_one', methods=['GET'])
@cross_origin()
def find_one():
    myCollection = mongo.db.patient
    query = myCollection.find_one()
    output = {
        "patient_room": query["patient_room"],
        "patient": query["patient"]
    }

    return output


@app.route('/create_patient', methods=['POST'])
@cross_origin()
def patient():
    myCollection = mongo.db.patient
    data = request.json
    myInsert = {
        "patient_room": data["patient_room"],
        "status": data["status"],
        "doctor": data["doctor"],
        "patient": data["patient"]
    }
    myCollection.insert_one(myInsert)
    return {"result": "Create succesfully"}


@app.route('/hw_status', methods=['GET'])
@cross_origin()
def hw_status():
    myCollection_queue = mongo.db.queue_robot
    myCollection_robot = mongo.db.status_robot
    myCollection_status = mongo.db.get_status
    data = myCollection_queue.find_one()
    robot = myCollection_robot.find_one()
    status = myCollection_status.find_one()
    if data == None and robot == None:
        filt = {"patient_room" : status["patient_room"]}
        updated_content = {"$set": {
            "patient_room" : "?",
            "status" : "-"
        }}
        myCollection_status.update_one(filt, updated_content)
    elif status["status"] == "receive":
        filt_status = {"patient_room" : robot["patient_room"]}
        filt = {"patient_room" : status["patient_room"]}
        updated_content = {"$set": {
            "patient_room" : "?",
            "status" : "-"
        }}
        myCollection_status.update_one(filt, updated_content)
        myCollection_robot.delete_one(filt_status)
    elif status != None:
        filt = {"patient_room" : status["patient_room"]}
        updated_content = {"$set": {
            "patient_room" : robot["patient_room"],
            "status" : robot["status"]
        }}
        myCollection_status.update_one(filt, updated_content)
    status = myCollection_status.find_one()
    return {"stauts" : status["status"]}


@app.route('/hw_return', methods=['PUT'])
@cross_origin()
def hw_return():
    myCollection_queue = mongo.db.queue_robot
    myCollection_robot = mongo.db.status_robot
    data = myCollection_queue.find_one()
    status = myCollection_robot.find_one()
    filt = {"patient_room" : status["patient_room"]}
    updated_content = {"$set": {
        "patient_room" : status["patient_room"],
        "status" : "receive"
    }}
    myCollection_robot.update_one(filt, updated_content)
    return {"result" : "Update successfully"}


@app.route('/hw_get', methods=['GET'])
@cross_origin()
def hw_get():
    myCollection_queue = mongo.db.queue_robot
    myCollection_robot = mongo.db.status_robot
    data = myCollection_queue.find_one()
    status = myCollection_robot.find_one()
    output = []
    if data != None:
        filt = {"patient_room" : data["patient_room"]}
        data_filt = int(data["patient_room"])
        myCollection_queue.delete_one(filt)
        updated_content = {"$set": {
            "patient_room" : data["patient_room"],
            "status" : "destination"
        }}
        myCollection_robot.update_one(filt, updated_content)
    else:
        filt = []
        data_filt = []
    if status["status"] == "receive":
        filt_status = {"patient_room" : status["patient_room"]}
        myCollection_robot.delete_one(filt_status)
    return {"data" : data_filt}


@app.route('/hw_post', methods=['POST'])
@cross_origin()
def hw_post():
    myCollection_queue = mongo.db.queue_robot
    myCollection_robot = mongo.db.status_robot
    data = request.json
    myInsert_queue = {
        "patient_room" : data["patient_room"]
    }
    myInsert_robot = {
        "patient_room" : data["patient_room"],
        "status" : "start"
    }
    myCollection_queue.insert_one(myInsert_queue)
    myCollection_robot.insert_one(myInsert_robot)
    return {"result" : "Create successfully"}


if __name__ == "__main__":
    app.run(host='0.0.0.0', port='3000', debug=True)
