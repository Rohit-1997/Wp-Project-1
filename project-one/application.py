# importing the modules
import os
from flask import Flask, render_template, redirect, url_for, flash, session, request
from flask_sqlalchemy import SQLAlchemy
from models import *

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
    if request.method == "POST":
        user_name = request.form.get('reg-username')
        email = request.form.get('reg-mail')
        password = request.form.get('reg-password')

        # adding the details to the database
        try:
            user = User(username=user_name, email=email, password=password)
            db.session.add(user)
            db.session.commit()
            flash(f'Created account for {user.username}', 'success')
            return redirect(url_for('login'))
        except Exception as e:
            print(str(e))
            flash(f'Not able to create the account at the moment, please try later', 'danger')
            return redirect(url_for('register'))
    return render_template('test_registration.html', title="Register")


# the login route
@app.route("/login", methods=['GET','POST'])
def login():
    if request.method == "POST":
        email = request.form.get("mail")
        password = request.form.get("password")
        print(password)
        # get the creds from the database
        user = User.query.filter_by(email=email).first()
        print(user.password)
        if user and user.password == password:
            # setting up the session varaible
            session["USERNAME"] = user.username
            flash('login succecssful', 'success')
            return redirect(url_for('profile'))
        else:
            flash('login not succecssful', 'danger')
    return render_template('test_login.html', title='Login')


# the profile route
@app.route("/profile")
def profile():
    # check if the user is in the session
    if session.get("USERNAME") is not None:
        user_name = session.get("USERNAME")
        user = User.query.filter_by(username=user_name).first()
        print(user.username)
        return render_template("profile.html", title="Profile Page", user=user_name)
    else:
        flash('No user in the session', 'danger')
        return redirect(url_for('login'))


# the sign out route
@app.route("/logout")
def logout():
    session.pop("USERNAME", None)
    try:
        print("In logout",session.get("USERNAME"))
    except:
        print("got error")
    flash('Logout successful', 'success')
    return redirect(url_for('login'))



# The admin route
@app.route("/admin")
def admin():
    """
    Query the registration data and display to the end user
    """
    data = User.query.all()
    for ele in data:
        print(ele.username)
    return render_template('admin.html', data=data)



if __name__ == "__main__":
    app.run(debug=True)
