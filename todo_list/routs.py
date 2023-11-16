from datetime import datetime

from bson.objectid import ObjectId
from flask import render_template, request, redirect, url_for, flash, session, abort
from todo_list import app, Tasks, Users, login_required
from werkzeug.security import generate_password_hash, check_password_hash


@app.route('/', methods=['GET', 'POST'])
def index():
    if session.get('user'):
        user = session['user']
        if request.method == 'POST':
            Tasks.insert_one({'task': request.form['task'],
                              "date": datetime.now().strftime('%d-%m-%Y'),
                              'user': user['_id']})
            flash("Task Added Successfully", "g")
            return redirect((url_for('index')))
        all_task = Tasks.find({"user": ObjectId(user['_id'])}).sort('_id')
        return render_template('index.html', tasks=all_task)
    return redirect(url_for('login'))


@app.route('/task-done')
@login_required
def task_done():
    flash('Task deleted', 'r')
    Tasks.delete_one({"_id": ObjectId(request.args["id"])})
    return redirect((url_for('index')))


@app.route('/update-task', methods=['POST', 'GET'])
@login_required
def update_task():
    if request.method == 'POST':
        Tasks.update_one({'_id': ObjectId(request.args['id'])},
                         {'$set': {'task': request.form['updated-task'],
                                   'date': datetime.now().strftime('%d-%m-%Y')}})
        flash('Task Updated Successfully', 'g')
        return redirect(url_for('index'))
    task = Tasks.find_one({'_id': ObjectId(request.args["id"])})
    return render_template('update_task.html', task=task)


@app.route('/login', methods=['POST', 'GET'])
def login():
    if session.get('user'):
        return redirect(url_for('index'))

    if request.method == 'POST':
        user = Users.find_one({'username': request.form.get('username')})
        if user:
            if check_password_hash(user['password'], request.form.get('password')):
                session['user'] = user
                flash('User Logged in Successfully', 'g')
                return redirect(url_for('index'))
            else:
                flash('Incorrect Password', 'r')
                return redirect(url_for('login'))
        else:
            flash('Username does not exist', 'r')
            return redirect(url_for('login'))
    return render_template('login.html')


@app.route('/logout')
@login_required
def logout():
    if session.get('user'):
        del session['user']
        return redirect(url_for('login'))


@app.route('/signup', methods=['POST', 'GET'])
def signup():
    if session.get('user'):
        return redirect(url_for('index'))

    if request.method == 'POST':
        if request.form.get('password') == request.form.get('c-password'):
            user_id = Users.insert_one({'Name': request.form.get('full_name'),
                                        'username': request.form.get('username'),
                                        'password': generate_password_hash(request.form.get("password"),
                                                                           salt_length=8)})
            session['user'] = Users.find_one({'_id': user_id.inserted_id})
            flash('User Signed up Successfully', 'g')
            return redirect(url_for('index'))
        else:
            flash('Password not match', 'r')
            return redirect(url_for('signup'))
    return render_template('signup.html')
