# importing the modules
import os
from flask import Flask, render_template, redirect, url_for, flash, session
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
        try:
            db_helper = DB_Helper(db,User)
            db_helper.add_record(reg_form)
            flash(f'Created account for {reg_form.username.data}', 'success')
        except:
            flash(f'Not able to create the account at the moment, please try later', 'danger')
        return redirect(url_for('home'))
    return render_template('registration.html', title='Register', reg_form=reg_form)


# the login route
@app.route("/login", methods=['GET','POST'])
def login():
    login_form = LoginForm()
    if login_form.validate_on_submit():
        # validating the database
        user = User.query.filter_by(email=login_form.email.data).first()
        if user and user.password == login_form.password.data:
            # setting up the session varaible
            session["USERNAME"] = user.username
            return redirect(url_for('profile'))
        else:
            flash('login not succecssful', 'danger')
    return render_template('login.html', title='Login', login_form=login_form)


# the profile route
@app.route("/profile")
def profile():
    # check if the user is in the session
    if session.get("USERNAME") is not None:
        user_name = session.get("USERNAME")
        user = User.query.filter_by(username=user_name).first()
        flash('Login successful', 'success')
        print(user.username)
        return render_template("profile.html", title="Profile Page", user=user)
    else:
        flash('No user in the session', 'danger')
        return redirect(url_for('login'))


# the sign out route
@app.route("/logout")
def logout():
    session.pop("USERNAME", None)
    flash('Logout successful', 'success')
    return redirect(url_for('login'))



# The admin route
@app.route("/admin")
def admin():
    """
    Query the registration data and display to the end user
    """
    db_helper = DB_Helper(db,User)
    data = db_helper.query_records()
    for ele in data:
        print(ele.username)
    return render_template('admin.html', data=data)



if __name__ == "__main__":
    app.run(debug=True)
