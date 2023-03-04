from myproject import app,db
from flask import render_template, redirect, request, url_for, flash,abort
from flask_login import login_user,login_required,logout_user
from myproject.models import User,Student,Teacher,Class
from myproject.forms import LoginForm, RegistrationForm, AddForm, DeleteForm 
from werkzeug.security import generate_password_hash, check_password_hash
from flask_migrate import Migrate
import os
from flask_sqlalchemy import SQLAlchemy


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/welcome')
@login_required
def welcome_user():
    return render_template('welcome_user.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You logged out!')
    return redirect(url_for('home'))


@app.route('/login', methods=['GET', 'POST'])
def login():

    form = LoginForm()
    if form.validate_on_submit():
        # Grab the user from our User Models table
        user = User.query.filter_by(email=form.email.data).first()
        
        # Check that the user was supplied and the password is right
        # The verify_password method comes from the User object
        # https://stackoverflow.com/questions/2209755/python-operation-vs-is-not

        if user.check_password(form.password.data) and user is not None:
            #Log in the user

            login_user(user)
            flash('Logged in successfully.')

            # If a user was trying to visit a page that requires a login
            # flask saves that URL as 'next'.
            next = request.args.get('next')

            # So let's now check if that next exists, otherwise we'll go to
            # the welcome page.
            if next == None or not next[0]=='/':
                next = url_for('welcome_user')

            return redirect(next)
    return render_template('login.html', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()

    if form.validate_on_submit():
        user = User(email=form.email.data,
                    username=form.username.data,
                    password=form.password.data)

        db.session.add(user)
        db.session.commit()
        flash('Thanks for registering! Now you can login!')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route('/add_student')
def add_student():
    return render_template("add_student.html")

@app.route("/saverecord",methods = ["POST","GET"])
def saverecord():
    msg = "msg"
    form = AddForm()
    # if form.validate_on_submit():
    if request.method == "POST": 
        try: 
            # Class= Class(Class="One")
            student = Student(name = "Jose",
                        email = "jose@email.com",
                        gender="male",
                        contact="1245780",
                        # dob=form.dob.data,
                        address="gurgaon.harayana",
                        Class="Fifth") 
            # db.engine.execute(Student.insert(student))

            db = SQLAlchemy(app)
            Migrate(app,db)
            db.session.add(student)
            db.session.commit()

            msg = "Student details successfully Added"
        except:
            msg = "Student Detail's not added to database"
        finally:
            return render_template("success_record.html",msg = msg,form=form)
    

@app.route('/student_info')
def view_details():
    basedir = os.path.abspath(os.path.dirname(__file__))
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db = SQLAlchemy(app)
    Migrate(app,db) 
            
    students=Student.query.all()
    return render_template("student_info.html")


@app.route("/delete_student")
def delete_student():
    return render_template("delete_student.html")

@app.route("/deleterecord",methods = ["GET","POST"])
def deleterecord():
    msg = "msg"
    try:
            id = Student.query.filter_by(id=Student.id).first()
            basedir = os.path.abspath(os.path.dirname(__file__))
            app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
            app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

            db = SQLAlchemy(app)
            Migrate(app,db) 
            
            if Student:

                db.session.delete(id)
                db.session.commit()
            msg = "Student detail successfully deleted"
            return render_template("delete_record.html", msg=msg)
    except:
            msg = "Can't delete student detail"
            return render_template("delete_record.html",msg=msg)
    finally:
            return render_template("delete_record.html", msg=msg)


if __name__ == '__main__':
    app.run(debug=True)
