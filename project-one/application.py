# importing the modules
import os, json
from flask import Flask, render_template, redirect, url_for, flash, session, request, jsonify
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

# the api_key
api_key = "Hs4Jb2udCEGREnCtluAzqA"


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

    # check if the drop down value is selected or not
    if dropdown_data is None or search_data == "":
        flash('Please select the search option or type in the words', 'danger')
        return redirect(url_for('book_search'))

    # querying the data
    search_data= f"{search_data}%"         # this is the formatted version for querying
    try:
        book_data = Books.query.filter(getattr(Books,dropdown_data).like(search_data)).all()
        return render_template('profile.html', title="Profile Page", book_data=book_data, user=session.get("USERNAME"), did_query=True)
    except Exception as e:
        print(str(e))
        flash('No data for the search', 'danger')
        return redirect(url_for('book_search'))


# the book details page
@app.route("/books/<isbn>", methods=["GET","POST"])
def book_details(isbn):
    print(isbn)
    # querying the database
    book = Books.query.filter_by(isbn=isbn).first()             # query the book based on isbn
    reviews = Reviews.query.filter_by(book_isbn=isbn).all()     # query for the reviews that were given on that book
    if request.method == "POST":
        review_data = request.form.get("post-review-data")
        rating_data = request.form.get("rating-value")

        # testing the edge cases if the users submit without writing the review
        if review_data == "" or rating_data is None:
            flash('Please enter the data in the review box or select the rating', 'danger')
            return redirect(url_for('book_details', isbn=isbn))

        # creating the review object to insert the into the database
        try:
            review = Reviews(book_isbn=book.isbn, user_name=session.get("USERNAME"), rating=int(rating_data), review=review_data)
            db.session.add(review)
            db.session.commit()
            return redirect(url_for('book_details', isbn=isbn))
        except Exception as e:
            print(str(e))
            flash('You have submitted your review already', 'danger')
            return redirect(url_for('book_details', isbn=isbn))
    return render_template('book.html', book=book, reviews=reviews)

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
    data = User.query.order_by(User.register_date.desc()).all()
    for ele in data:
        print(ele.username)
    return render_template('admin.html', data=data)


# The api route
@app.route("/api/<string:isbn>")
def api_call(isbn):
    # check to see if the isbn exists
    book = Books.query.get(isbn)
    if book is None:
        return jsonify({"error": "Invalid ISBN number"}), 404

    # making api call
    res = requests.get("https://www.goodreads.com/book/review_counts.json", params={"key": api_key, "isbns": isbn})
    res_json = res.json()
    print(res_json)
    return jsonify({
        "title": book.title,
        "author": book.author,
        "year": book.year,
        "isbn": isbn,
        "review_count": res_json["books"][0]["reviews_count"],
        "average_score": res_json["books"][0]["average_rating"]
    })

@app.route("/userhome")
def home_API():
    if session.get("USERNAME") is  None:
        flash('No user in the session', 'danger')
        return redirect(url_for('login'))
    else:
        return render_template('home_API.html', user=session.get("USERNAME"))

@app.route("/api/search/isbn", methods=["POST"])
def search_api():
    # get the form data
    isbn = request.form.get("isbn")
    print("The isbn value: ", isbn)
    search_isbn = f'{isbn}%'
    books = Books.query.filter(Books.isbn.like(search_isbn)).all()
    print(books)
    if books is None or books == []:
        return jsonify({"success": False}), 404

    books_searialized = []
    for book in books:
        dict_data = {}
        dict_data["title"] = book.title
        dict_data["author"] = book.author
        dict_data["isbn"] = book.isbn
        books_searialized.append(dict_data)

    print(books_searialized)
    return jsonify({
        "success": True,
        "books": books_searialized
    })




if __name__ == "__main__":
    app.run(debug=True)
