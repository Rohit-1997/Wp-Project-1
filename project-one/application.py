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
        # get the creds from the database
        user = User.query.filter_by(email=email).first()
        if user and user.password == password:
            # setting up the session varaible
            session["USERNAME"] = user.username
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

# the function to handle searchdata
@app.route("/profile", methods=['POST'])
def book_search():
    # get the text typed in by the user
    search_data = request.form.get('search-input')
    dropdown_data = request.form.get('dropdown-value')

    # querying the data
    search_data= f"{search_data}%"         # this is the formatted version for querying
    try:
        book_data = Books.query.filter(getattr(Books,dropdown_data).like(search_data)).all()
        return render_template('profile.html', title="Profile Page", book_data=book_data, user=session.get("USERNAME"), did_query=True)
    except Exception as e:
        print(str(e))
        flash('No data for the search', 'danger')
        return redirect(url_for('profile'))


# the book details page
@app.route("/books/<isbn>/<title>")
def book_details(isbn,title):
    print(isbn, title)
    book_data = Books.query.filter_by(isbn = isbn).first()
    reviews_list = Reviews.query.filter_by(book_isbn = isbn).all()
    # print(reviews_list)
    rating = 0
    count = 0
    for each in reviews_list:
        rating = rating + each.rating
        count = count + 1
    # print(rating//count)
    avg_rating = rating//count
    return render_template('book.html', title = book_data.title, isbn = book_data.isbn, author = book_data.author, year = book_data.year, reviews_list= reviews_list , avg_rating = avg_rating)

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
    data = User.query.all()
    for ele in data:
        print(ele.username)
    return render_template('admin.html', data=data)




if __name__ == "__main__":
    app.run(debug=True)
