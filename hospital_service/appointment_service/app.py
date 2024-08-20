from flask import Flask, request, jsonify, render_template
from flask_pymongo import PyMongo
from bson.objectid import ObjectId

app = Flask(__name__)
app.config['MONGO_URI'] = 'mongodb://localhost:27017/hospital_db'  # MongoDB connection URI
mongo = PyMongo(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/appointments', methods=['POST'])
def add_appointment():
    data = request.json
    appointment_id = mongo.db.appointments.insert_one({
        'patient_name': data['patient_name'],
        'date': data['date']
    }).inserted_id
    return jsonify({"message": "Appointment added", "id": str(appointment_id)}), 201

@app.route('/appointments', methods=['GET'])
def get_appointments():
    appointments = mongo.db.appointments.find()
    return jsonify([{"id": str(appt['_id']), "patient_name": appt['patient_name'], "date": appt['date']} for appt in appointments]), 200

@app.route('/appointments/<id>', methods=['PUT'])
def update_appointment(id):
    appointment = mongo.db.appointments.find_one({'_id': ObjectId(id)})
    if not appointment:
        return jsonify({"message": "Appointment not found"}), 404
    mongo.db.appointments.update_one({'_id': ObjectId(id)}, {'$set': {
        'patient_name': request.json['patient_name'],
        'date': request.json['date']
    }})
    return jsonify({"message": "Appointment updated"}), 200

@app.route('/appointments/<id>', methods=['DELETE'])
def delete_appointment(id):
    appointment = mongo.db.appointments.find_one({'_id': ObjectId(id)})
    if not appointment:
        return jsonify({"message": "Appointment not found"}), 404
    mongo.db.appointments.delete_one({'_id': ObjectId(id)})
    return jsonify({"message": "Appointment deleted"}), 200

if __name__ == '__main__':
    app.run(debug=True)
