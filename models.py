from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime

db=SQLAlchemy()

class User(UserMixin,db.Model):
    __tablename__='user'
    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(15), nullable=False)
    role = db.Column(db.String(50),nullable=False)

class Trekk_Staff(db.Model):
    __tablename__='Trekk_staff'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable = False)
    difficulty = db.Column(db.String(50))
    slots_available = db.Column(db.Integer,  nullable = False)
    status = db.Column(db.String(100), default = 'Open')
    mentor_id = db.Column(db.Integer, db.ForeignKey('user.id'))

class Booking(db.Model):
    __table__name='booking'
    id=db.Column(db.Integer, primary_key = True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    trek_id = db.Column(db.Integer, db.ForeignKey('Trekk_staff.id'))
    status = db.Column(db.String(50), default = 'Booked')

