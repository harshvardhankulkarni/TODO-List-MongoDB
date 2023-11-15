import os

from dotenv import load_dotenv
from flask import Flask
from flask_pymongo import PyMongo
from flask_session import Session

app = Flask(__name__)

load_dotenv()

app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

app.config["MONGO_URI"] = os.getenv('MONGO_URI')
db = PyMongo(app).db

# Collections
Tasks = db.tasks
Users = db.users

Users.create_index('username', unique=True)

from todo_list import routs
