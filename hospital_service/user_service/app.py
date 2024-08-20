from flask import Flask, request, jsonify, render_template, session
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash
from bson.errors import InvalidId

app = Flask(__name__)
app.config['MONGO_URI'] = 'mongodb://localhost:27017/users_db'
app.secret_key = 'your_secret_key'  # Replace with a secure key
mongo = PyMongo(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['POST'])
def register():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    email = data.get('email')
    full_name = data.get('full_name')
    phone = data.get('phone')
    
    if not username or not password or not email or not full_name or not phone:
        return jsonify({"message": "All fields are required"}), 400
    
    existing_user = mongo.db.users.find_one({'username': username})
    if existing_user:
        return jsonify({"message": "User already exists"}), 409
    
    hashed_password = generate_password_hash(password)
    user_id = mongo.db.users.insert_one({
        'username': username,
        'password': hashed_password,
        'email': email,
        'full_name': full_name,
        'phone': phone
    }).inserted_id
    
    return jsonify({"message": "User registered", "id": str(user_id)}), 201

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    
    user = mongo.db.users.find_one({'username': username})
    if user and check_password_hash(user['password'], password):
        session['user_id'] = str(user['_id'])  # Store user ID in session
        return jsonify({
            "message": "Login successful", 
            "success": True,
            "user_data": {
                "id": str(user['_id']),
                "username": user['username'],
                "email": user['email'],
                "full_name": user['full_name'],
                "phone": user['phone']
            }
        }), 200
    else:
        return jsonify({"message": "Invalid username or password", "success": False}), 401

@app.route('/dashboard', methods=['GET'])
def dashboard():
    if 'user_id' not in session:
        return jsonify({"message": "Unauthorized access"}), 401

    user_id = session['user_id']
    user = mongo.db.users.find_one({"_id": ObjectId(user_id)})

    if not user:
        return jsonify({"message": "User not found"}), 404

    all_users = mongo.db.users.find()
    users_data = [{"id": str(user['_id']),
                   "username": user['username'],
                   "email": user['email'],
                   "full_name": user['full_name'],
                   "phone": user['phone']} for user in all_users]

    user_data = {
        "id": str(user['_id']),
        "username": user['username'],
        "email": user['email'],
        "full_name": user['full_name'],
        "phone": user['phone']
    }

    return render_template('dashboard.html', user=user_data, users=users_data)

@app.route('/users/<id>', methods=['PUT'])
def update_user(id):
    if not ObjectId.is_valid(id):
        return jsonify({"message": "Invalid user ID"}), 400

    data = request.json
    updates = {
        'username': data.get('username'),
        'email': data.get('email'),
        'full_name': data.get('full_name'),
        'phone': data.get('phone')
    }
    result = mongo.db.users.update_one({'_id': ObjectId(id)}, {'$set': updates})
    if result.matched_count == 0:
        return jsonify({"message": "User not found"}), 404
    return jsonify({"message": "User updated"}), 200

@app.route('/users/<id>', methods=['DELETE'])
def delete_user(id):
    if not ObjectId.is_valid(id):
        return jsonify({"message": "Invalid user ID"}), 400

    result = mongo.db.users.delete_one({'_id': ObjectId(id)})
    if result.deleted_count == 0:
        return jsonify({"message": "User not found"}), 404
    return jsonify({"message": "User deleted"}), 200

@app.route('/users', methods=['GET'])
def get_users():
    users = mongo.db.users.find()
    users_data = []
    
    for user in users:
        user_data = {
            "id": str(user['_id']),
            "username": user['username'],
            "email": user['email'],
            "full_name": user['full_name'],
            "phone": user['phone']
        }
        users_data.append(user_data)
    
    return jsonify(users_data), 200


if __name__ == "__main__":
    app.run(debug=True)
