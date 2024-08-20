from flask import Flask, request, jsonify, render_template
from flask_pymongo import PyMongo
from bson.objectid import ObjectId

app = Flask(__name__)
app.config['MONGO_URI'] = 'mongodb://localhost:27017/hospital_db'  # MongoDB connection URI
mongo = PyMongo(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/patients', methods=['POST'])
def add_patient():
    data = request.json
    patient_id = mongo.db.patients.insert_one({'name': data['name']}).inserted_id
    return jsonify({"message": "Patient added", "id": str(patient_id)}), 201

@app.route('/patients', methods=['GET'])
def get_patients():
    patients = mongo.db.patients.find()
    return jsonify([{"id": str(patient['_id']), "name": patient['name']} for patient in patients]), 200

@app.route('/patients/<id>', methods=['PUT'])
def update_patient(id):
    patient = mongo.db.patients.find_one({'_id': ObjectId(id)})
    if not patient:
        return jsonify({"message": "Patient not found"}), 404
    mongo.db.patients.update_one({'_id': ObjectId(id)}, {'$set': {'name': request.json['name']}})
    return jsonify({"message": "Patient updated"}), 200

@app.route('/patients/<id>', methods=['DELETE'])
def delete_patient(id):
    patient = mongo.db.patients.find_one({'_id': ObjectId(id)})
    if not patient:
        return jsonify({"message": "Patient not found"}), 404
    mongo.db.patients.delete_one({'_id': ObjectId(id)})
    return jsonify({"message": "Patient deleted"}), 200

if __name__ == '__main__':
    app.run(debug=True)
