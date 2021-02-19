from flask import Flask, request, Response, jsonify
from flask_pymongo import PyMongo
import json

from flask_cors import CORS, cross_origin

app = Flask(__name__)
cors = CORS(app, resources={r"/": {"origins": "*"}})
app.config['MONGO_URI'] = 'mongodb://exceed_group13:zb924yhy@158.108.182.0:2255/exceed_group13'
mongo =PyMongo(app)


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
    return Response(json.dumps(output),  mimetype='application/json')


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


@app.route('/hw_get', methods=['GET'])
@cross_origin()
def hw_get():
    myCollection = mongo.db.hardware
    data = myCollection.find_one()
    output = []
    if data != None:
        filt = {"patient_room" : data["patient_room"]}
        myCollection.delete_one(filt)
        query = myCollection.find()
        for ele in query:
            output.append({
                "patient_room" : ele["patient_room"]
            })
    else:
        filt = []
    return {"result" : output, "data" : filt}


@app.route('/hw_post', methods=['POST'])
@cross_origin()
def hw_post():
    myCollection = mongo.db.hardware
    data = request.json
    myInsert = {
        "patient_room" : data["patient_room"]
    }
    myCollection.insert_one(myInsert)
    return {"result" : "Create successfully"}


if __name__ == "__main__":
    app.run(host='0.0.0.0', port='3000', debug=True)