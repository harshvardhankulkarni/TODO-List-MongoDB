from datetime import datetime

from bson.objectid import ObjectId
from flask import render_template, request, redirect, url_for, flash

from todo_list import app, Tasks


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        Tasks.insert_one({'task': request.form['task'],
                          "date": datetime.now().strftime('%d-%m-%Y')})
        flash("Task Added Successfully", "success")
        return redirect((url_for('index')))
    all_task = Tasks.find().sort('_id')
    return render_template('index.html', tasks=all_task)


@app.route('/task-done')
def task_done():
    flash('Task deleted')
    Tasks.delete_one({"_id": ObjectId(request.args["id"])})
    return redirect((url_for('index')))


@app.route('/update-task', methods=['POST', 'GET'])
def update_task():
    if request.method == 'POST':
        Tasks.update_one({'_id': ObjectId(request.args['id'])},
                         {'$set': {'task': request.form['updated-task'],
                                   'date': datetime.now().strftime('%d-%m-%Y')}})
        flash('Task Updated Successfully', 'success')
        return redirect(url_for('index'))
    task = Tasks.find_one({'_id': ObjectId(request.args["id"])})
    return render_template('update_task.html', task=task)
