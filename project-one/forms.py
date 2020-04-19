from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from models import User

# the refistration form
class RegistrationForm(FlaskForm):
    # the fields that are required for this form
    username = StringField('Username',validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), Length(min=8), EqualTo('password')])
    submit = SubmitField('Sign up')

    # validating to check the users do not enter duplicate values for user names and emails
    def validate_username(self,username):
        # check the database
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError("This user name is take, Please choose another one")

    def validate_email(self,email):
        # check the database
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError("This email is taken, Please choose a different one")


# The login form
class LoginForm(FlaskForm):
    # the fields that are required for this form
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8)])
    submit = SubmitField('Login')
