from flask import Flask, request, Response
from flask_pymongo import PyMongo
import json

app = Flask(__name__)
app.config['MONGO_URI'] = 'mongodb://exceed_group13:zb924yhy@158.108.182.0:2255/exceed_group13'
mongo =PyMongo(app)

# myCollection = mongo.db.patient


@app.route('/test', methods=['GET'])
def hello():
    return {'res': 'hello world'}


@app.route('/find_all', methods=['GET'])
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
def find_patient():
    myCollection = mongo.db.patient
    myName = request.args.get("patient_room")
    if myName != None:
        flit = {"patient_room": int(myName)}
        query = myCollection.find(flit)
    else:
        query = myCollection.find()
    output = []
    for ele in query:
        output.append({
            "patient_room": ele["patient_room"],
            "status": ele["status"],
            "doctor": ele["doctor"],
            "patient": ele["patient"]
        })
    return Response(json.dumps(output),  mimetype='application/json')


@app.route('/find_one', methods=['GET'])
def find_one():
    myCollection = mongo.db.patient
    query = myCollection.find_one()
    output = {
            "patient_room": query["patient_room"],
            "status": query["status"],
            "doctor": query["doctor"],
            "patient": query["patient"]
            }

    return output


@app.route('/create_patient', methods=['POST'])
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


if __name__ == "__main__":
    app.run(host='0.0.0.0', port='3000', debug=True)