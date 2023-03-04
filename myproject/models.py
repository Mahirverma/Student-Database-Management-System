from myproject import db,login_manager
import os
from flask import Flask
from flask_sqlalchemy import *
from flask_migrate import Migrate
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin

# By inheriting the UserMixin we get access to a lot of built-in attributes
# which we will be able to call in our views!
# is_authenticated()
# is_active()
# is_anonymous()
# get_id()


# The user_loader decorator allows flask-login to load the current user
# and grab their id.
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

class User(db.Model, UserMixin):

    # Create a table in the db
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key = True)
    email = db.Column(db.String(64), unique=True, index=True)
    username = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))

    def __init__(self, email, username, password):
        self.email = email
        self.username = username
        self.password_hash = generate_password_hash(password)

    def check_password(self,password):
        # https://stackoverflow.com/questions/23432478/flask-generate-password-hash-not-constant-output
        return check_password_hash(self.password_hash,password)

#another table for the records of students
class Student(db.Model):
    __tablename__='students'

    id=db.Column(db.Integer, primary_key = True)
    name=db.Column(db.String(255))
    email=db.Column(db.String(255),unique=True)
    gender=db.Column(db.String(50))
    contact=db.Column(db.String(12))
    # dob=db.Column(db.Date)
    address=db.Column(db.Text)
    Class=db.Column(db.String(10))

    def __init__(self,name,email,gender,contact,dob,address,Class):
        self.name=name
        self.email=email
        self.gender=gender
        self.contact=contact
        # self.dob=dob
        self.address=address
        self.Class=Class
   
class Class(db.Model):
    __tablename__='class'

    id=db.Column(db.Integer,primary_key=True)
    Class=db.Column(db.String(10))
    teachers=db.relationship('Teacher',backref='class')

class Teacher(db.Model):
    __tablename__='teachers'

    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(50))
    subject=db.Column(db.String(50))
    Class=db.Column(db.String(10),db.ForeignKey('class.id'))

    def __init__(self,name,subject):
        self.name=name
        self.subject=subject