from flask import Flask
from flask_sqlalchemy import SQLAlchemy

mn=Flask(__name__)

db=SQLAlchemy(mn)


mn.config['SECRET_KEY'] = "helloworldkllk"
mn.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test2.db'

class Admin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    admin_username = db.Column(db.String(100), nullable=False, unique=True)
    admin_password = db.Column(db.String(200), nullable=False)
    
    
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    user_name = db.Column(db.String(100), nullable=False, unique=True)
    user_password = db.Column(db.String(200), nullable=False)
    # user_book=db.relationship("Booking", backref="user",cascade="all, delete")