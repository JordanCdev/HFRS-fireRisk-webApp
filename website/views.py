from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from flask_mysqldb import MySQL
from .models import Note
from . import db
from . import mysql
import json
import pickle
import numpy as np
import csv


views = Blueprint('views', __name__)
classifier = pickle.load(open('website/iris.pkl', 'rb'))

@views.route('/', methods=['GET', 'POST'])
@login_required #must be logged in to access page
def home():
    if request.method == 'POST':
        note = request.form.get('note')
        
        if len(note) == 0:
            flash("Note is empty.", category='error')
        else:
            new_note = Note(data=note, user_id=current_user.id) 
            db.session.add(new_note)
            db.session.commit()
            flash("Note added.", category='success')
    return render_template("home.html", user=current_user)

@views.route('/delete-note', methods=['POST'])
def delete_note():
    note = json.loads(request.data)
    noteId = note['noteId']
    note = Note.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()

    return jsonify({})

@views.route('/train', methods=['GET', 'POST'])
@login_required #must be logged in to access page
def train(): 
    if request.method == 'POST':
        data1 = request.form['a']
        data2 = request.form['b']
        data3 = request.form['c']
        data4 = request.form['d']
        arr = np.array([[data1, data2, data3, data4]])
        pred = classifier.predict(arr)
        return render_template('train.html', user=current_user, data=pred)
    else:
        return render_template('train.html', user=current_user)

@views.route('/predictions', methods=['GET', 'POST'])
@login_required
def predictions():
    conn = mysql.connection
    cur = conn.cursor()
    #cur.execute('''CREATE TABLE predictions (id int(20), Organisation VARCHAR(200), UPRN int(20), Risk int(10), PRIMARY KEY(id))''')
    #cur.execute('''SELECT * FROM predictions''')
    #results = cur.fetchall()
    #print(results)
    
    if request.method == 'POST':
        predictions = request.form['predictions']
        cur.execute('''select * from predictions where Organisation LIKE %s''', [predictions])
        conn.commit()
        data = cur.fetchall()
        print(data)
        if len(data) == 0 and predictions == 'all':
            cur.execute("SELECT * FROM predictions")
            conn.commit()
            data = cur.fetchall()
        return render_template("predictions.html", data=data, user=current_user)
    return render_template("predictions.html", user=current_user)