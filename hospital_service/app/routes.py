# app/routes.py
from flask import jsonify, request
from app import app, mongo

@app.route('/patients', methods=['GET'])
def get_patients():
    patients = list(mongo.db.patients.find())
    for patient in patients:
        patient['_id'] = str(patient['_id'])
    return jsonify(patients), 200
