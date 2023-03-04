from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField,SelectField,TextAreaField
from wtforms.validators import DataRequired,Email,EqualTo
from wtforms import ValidationError
from myproject.models import User

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Log In')


class RegistrationForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(),Email()])
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired(), EqualTo('pass_confirm', message='Passwords Must Match!')])
    pass_confirm = PasswordField('Confirm password', validators=[DataRequired()])
    submit = SubmitField('Register!')

    def validate_email(self, email):
        if User.query.filter_by(email=self.email.data).first():
            raise ValidationError('Email has been registered')
    def validate_username(self, username):
        if User.query.filter_by(username=self.username.data).first():
            raise ValidationError('Username has been registered')

class AddForm(FlaskForm):
    name=StringField('Name',validators=[DataRequired()])
    email=StringField('Email',validators=[DataRequired(),Email()])
    gender=SelectField('Gender', validators=[DataRequired()])
    contact=StringField('Contact',validators=[DataRequired()])
    # dob=StringField('D.O.B',validators=[DataRequired()])
    address=TextAreaField('Address',validators=[DataRequired()])
    Class=SelectField('Class', validators=[DataRequired()])
    submit= SubmitField('Submit')

class DeleteForm(FlaskForm):
    student_id=StringField("Student Id",validators=[DataRequired()])
    submit= SubmitField('Submit')
    def validate_student(self,student_id):
        if User.query.filter_by(student_id=self.id.data).first():
            raise ValidationError('NO Student with this Id!')

