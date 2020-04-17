# importing the modules
import os
from flask import Flask, render_template, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from forms import RegistrationForm, LoginForm
from models import *
from database_helper import DB_Helper

# creating an instance of Flask
app = Flask(__name__)

# setting up the secret key for the application
app.config['SECRET_KEY'] = 'f9a1520561f1faf67f36a3a620a45e80'

# setting up the database and database instance
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)

# The home page function
@app.route("/")
@app.route("/home")
def home():
    return render_template("home.html", title="Home")


@app.route("/register", methods=['GET','POST'])
def register():
    reg_form = RegistrationForm()
    # if the user is valid he will be redirected to the login page
    if reg_form.validate_on_submit():
        # adding the data to the Database
        db_helper = DB_Helper(db)
        db_helper.add_record(reg_form)
        flash(f'Created account for {reg_form.username.data}', 'success')
        return redirect(url_for('home'))
    return render_template('registration.html', title='Register', reg_form=reg_form)


# the login route
@app.route("/login", methods=['GET','POST'])
def login():
    login_form = LoginForm()
    if login_form.validate_on_submit():
        if login_form.email.data == "kalorirohit@gmail.com" and login_form.password.data == 'tunafish':
            flash('You have logged in successfuly!', 'success')
            return redirect(url_for('home'))
        else:
            flash('login not succecssful', 'danger')
    return render_template('login.html', title='Login', login_form=login_form)



if __name__ == "__main__":
    app.run(debug=True)
