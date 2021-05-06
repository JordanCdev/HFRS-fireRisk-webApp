from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True)
    password = db.Column(db.String(64))
    firstName = db.Column(db.String(32))
    notes = db.relationship('Note')

class Predictions(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ORGINISATION = db.Column(db.String(64), unique=True)
    UPRN = db.Column(db.Integer, unique=True)
    y_test = db.Column(db.Integer)