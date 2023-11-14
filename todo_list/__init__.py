from flask import Flask
from flask_pymongo import PyMongo
from flask_session import Session

app = Flask(__name__)
app.config['SECRET_KEY'] = 'SECRET_KEY'

app.secret_key = "Something Unique"
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

USERNAME = open('./todo_list/USERNAME.txt', 'r').read()
PASSWORD = open('./todo_list/PASSWORD.txt', 'r').read()
app.config["MONGO_URI"] = f'mongodb+srv://{USERNAME}:{PASSWORD}@firstmongoproject.aovehzm.mongodb.net/todo_list'
db = PyMongo(app).db

# Collections
Tasks = db.tasks
Users = db.users

Users.create_index('username', unique=True)

from todo_list import routs
