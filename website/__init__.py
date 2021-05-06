from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager
import csv 
import sqlite3
import pandas as pd
import sqlalchemy.dialects.mysql.mysqldb as MySQLdb
import yaml

db = SQLAlchemy()
DB_NAME = "database.db"
db2 = yaml.load(open('db.yaml'))

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'HFRS2021'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    app.config['MYSQL_HOST'] = db['mysql_host']
    app.config['MYSQL_USER'] = db['mysql_user']
    app.config['MYSQL_PASSWORD'] = db['mysql_password']
    app.config['MYSQL_DB'] = db['mysql_db']
    db.init_app(app)

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    from .models import User, Note, Predictions
    create_database(app)
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)
    parseCSV()

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id)) #looks for primary key in db
    return app

    

#checks if database exists, if not creates it
def create_database(app):
    if not path.exists('website/' + DB_NAME):
        db.create_all(app=app)
        print('Created Database!')

def parseCSV():
      # CVS Column Names
    col_names = ['ORGANISATION','UPRN','y_test']
      # Use Pandas to parse the CSV file
    csvData = pd.read_csv('website\static\predictions\Res_10_AB300_6y20112016_1y20172017_2021-05-05 1128PM.csv', names=col_names, header=None)
      # Loop through the Rows
    for i,row in csvData.iterrows():
             print(i,row['ORGANISATION'],row['UPRN'],row['y_test'],)    
    mydb = MySQLdb.connect(host="localhost", user="root", password="", database="predictions")
    with open('website\static\predictions\results.csv') as csv_file:
        csvfile = csv.reader(csv_file, delimiter=',')
        all_value = []
        for row in csvfile:
            value = (row[0], row[1], row[2], row[4])
            all_value.append(value)
    query = "insert into tbl 'predictions_db'('id', 'Organisation', 'UPRN', 'Risk')"
