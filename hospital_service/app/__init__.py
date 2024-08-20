# app/__init__.py
from flask import Flask
from flask_pymongo import PyMongo

app = Flask(__name__)
app.config.from_object('app.config.Config')

mongo = PyMongo(app)

# Import routes after initializing app and mongo
from app import routes

if __name__ == "__main__":
    app.run(debug=True)
