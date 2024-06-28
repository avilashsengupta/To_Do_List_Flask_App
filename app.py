from flask import Flask, render_template, redirect, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime as dt

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///project.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class ToDoList(db.Model):
    slno = db.Column(db.Integer, primary_key = True)
    text = db.Column(db.String(100), nullable = False)
    date = db.Column(db.String(10), nullable = False)
    time = db.Column(db.String(8), nullable = False)
    stat = db.Column(db.String(12), nullable = False)

@app.route('/')
def homepage():
    tlrcd = ToDoList.query.all()
    nwrcd = ToDoList.query.filter_by(stat = 'New').all()
    iprcd = ToDoList.query.filter_by(stat = 'In Progress').all()
    cmrcd = ToDoList.query.filter_by(stat = 'Completed').all()

    return render_template(
        'home.html',
        total_data = len(tlrcd),
        new_data = len(nwrcd),
        progress_data = len(iprcd),
        complete_data = len(cmrcd),
        full_list = tlrcd
    )

@app.route('/create', methods = ['GET','POST'])
def create_task():
    hours_option = []
    minutes_option = []

    for i in range(12):
        if i < 9: k = '0' + str(i+1)
        else: k = str(i+1)
        hours_option.append(k)
    
    for i in range(60):
        if i < 10: k = '0' + str(i)
        else: k = str(i)
        minutes_option.append(k)
    
    if request.method == 'POST':
        user_time = dt(
            hour = int()
        )

        todo = ToDoList(
            slno = len(ToDoList.query.all()) + 1,
            text = request.form['task'],
            date = request.form['date'],
            time = request.form['hour'] + ':' + request.form['minute'] + ' ' + request.form['maritime'],
            stat = 'New'
        )
        db.session.add(todo)
        db.session.commit()
    
    return render_template(
        'create.html',
        hours = hours_option,
        minutes = minutes_option,
        h_value = dt.now().strftime('%I'),
        m_value = dt.now().strftime('%M'),
        t_value = dt.now().strftime('%p')
    )

@app.route('/update/<int:taskno>', methods = ['GET','POST'])
def update_task(taskno):
    if request.method == 'POST':
        todo = ToDoList.query.filter_by(slno = taskno).first()
        todo.text = request.form['rename_task']
        db.session.add(todo)
        db.session.commit()
        return redirect('/')
    
    todo = ToDoList.query.filter_by(slno = taskno).first()
    return render_template(
        'update.html',
        task = todo
    )

@app.route('/status/<int:taskno>', methods = ['GET','POST'])
def update_stat(taskno):
    if request.method == 'POST':
        todo = ToDoList.query.filter_by(slno = taskno).first()
        if todo.stat == 'New': todo.stat = 'In Progress'
        elif todo.stat == 'In Progress': todo.stat = 'Completed'
        todo.date = dt.now().strftime('%Y') + '-' + dt.now().strftime('%m') + '-' + dt.now().strftime('%d')
        todo.time = dt.now().strftime('%I') + ':' + dt.now().strftime('%M') + ' ' + dt.now().strftime('%p')
        db.session.add(todo)
        db.session.commit()
    return redirect('/')

@app.route('/delete/<int:taskno>', methods = ['GET','POST'])
def delete_task(taskno):
    todo = ToDoList.query.filter_by(slno = taskno).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect('/')

with app.app_context(): db.create_all()
if __name__ == '__main__': app.run(debug = True)