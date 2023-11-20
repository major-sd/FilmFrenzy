from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from sqlalchemy.sql import func



db=SQLAlchemy() #initialise db under sqlalchemy



    
    
class User(db.Model,UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    username = db.Column(db.String(100), nullable=False, unique=True)
    userpassword = db.Column(db.String(200), nullable=False)
    admin = db.Column(db.Boolean, nullable=False, default=0)
    
    booking=db.relationship("Booking", backref="user",cascade="all, delete")
    rating=db.relationship("Usr", backref="user",cascade="all, delete")
    
    def __repr__(self) :
       return f"<User {self.name}- Admin: {self.admin}>"
    


class Venue(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(100), nullable=False)
    capacity = db.Column(db.Integer)
    vimg=db.Column(db.String(2000))
    
    shows=db.relationship("Show", backref="venue",cascade="all, delete")
    # show_cap=db.relationship("Show", backref="capacity",cascade="all, delete")
    booking=db.relationship("Booking", backref="venue",cascade="all, delete")
    # book_loc=db.relationship("Booking", cascade="all, delete")

    def __repr__(self) :
       return f"<Venue {self.name} >"


class Show(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    avg_rating = db.Column(db.Float)
    tags = db.Column(db.String(100))
    price = db.Column(db.Integer, nullable=False)
    show_timing = db.Column(db.String(20), nullable=False)
    venue_id = db.Column(db.Integer, db.ForeignKey('venue.id'), nullable=False) # pass venue obj here to gain access to all fields (wherever there is foreign key links)
    show_capacity = db.Column(db.Integer, nullable=False)
    simg=db.Column(db.String(2000))
    
    
    booking=db.relationship("Booking", backref="show",cascade="all, delete") # this will return a list of booking object for a given show
    ratings=db.relationship("Usr", backref="show",cascade="all, delete")
    
    def __repr__(self) :
       return f"<Show {self.name} >"
    
    
    
class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer,db.ForeignKey('user.id'), nullable=False)
    venue_id = db.Column(db.Integer,db.ForeignKey('venue.id'), nullable=False)
    show_id = db.Column(db.Integer,db.ForeignKey('show.id'), nullable=False)
    seats_book = db.Column(db.Integer)
    total_price=db.Column(db.Integer)
    # location=db.Column(db.String(100), db.ForeignKey('venue.location'), nullable=False)

#user_show_rating(Usr) schema
class Usr(db.Model): 
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer,db.ForeignKey('user.id'), nullable=False)
    # venue_id = db.Column(db.Integer,db.ForeignKey('venue.id'), nullable=False)
    show_id = db.Column(db.Integer,db.ForeignKey('show.id'), nullable=False)
    ratings= db.Column(db.Integer)
    # seats_book = db.Column(db.Integer)
    # total_price=db.Column(db.Integer)
    
    