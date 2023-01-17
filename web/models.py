from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50), unique=True)
    firstName = db.Column(db.String(30))
    lastName = db.Column(db.String(50))
    password = db.Column(db.String(30))
    passwords = db.relationship('Vault')

class Vault(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    userID = db.Column(db.Integer, db.ForeignKey('user.id'))
    service = db.Column(db.String(50))
    username = db.Column(db.String(50))
    passw = db.Column(db.String(150))
    date = db.Column(db.DateTime(timezone=True), default=func.now())