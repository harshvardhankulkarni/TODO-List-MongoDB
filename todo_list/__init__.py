from flask import Flask
from flask_pymongo import PyMongo

app = Flask(__name__)
app.config['SECRET_KEY'] = 'SECRET_KEY'
app.config["MONGO_URI"] = "mongodb://localhost:27017/todoList"
db = PyMongo(app).db

# Collections
Tasks = db.tasks
Users = db.users

from todo_list import routs
