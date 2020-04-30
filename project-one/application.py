# importing the modules
import os, requests,json
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
@app.route("/books/<isbn>" , methods = ['POST', 'GET'])
def book_details(isbn):
    # b = Books.query.filter_by(isbn = isbn).first()
    # r = Reviews.query.filter_by(book_isbn = isbn)
    if session.get("USERNAME") is  None:
        flash('No user in the session', 'danger')
        return redirect(url_for('login'))
    if request.method == 'POST':
        re = request.form.get('post-review-data')
        re1 = request.form.get('rating-value')
        try:
            if re != '' and  re1 != None :
                rev = Reviews(book_isbn = isbn, user_name = session.get("USERNAME"), rating = re1, review = re)
                db.session.add(rev)
                db.session.commit()
            else:
                flash('Please enter the data in the review box or select the rating', 'danger')
                return redirect(url_for('book_details', isbn=isbn))
                # return render_template('practice.html')
            return redirect(url_for('book_details', isbn=isbn))
        except Exception:
            flash('You have already reviewed it', 'danger')
            return redirect(url_for('book_details', isbn=isbn))

    else:
        if session.get("USERNAME") is not None: 
            b = Books.query.filter_by(isbn = isbn).first()
            r = Reviews.query.filter_by(book_isbn = isbn)
            return render_template('book.html', book = b, reviews =  r )
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
    data = User.query.all()
    for ele in data:
        print(ele.username)
    return render_template('admin.html', data=data)


# The user home page
@app.route("/userhome")
def user_home():
    if session.get("USERNAME") is  None:
        flash('No user in the session', 'danger')
        return redirect(url_for('login'))
    else:
        return render_template('user_home.html', user=session.get("USERNAME"))


# The api/search route to handle the search api request
@app.route("/api/search", methods=["POST"])
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

# Handling the route for book_details api
@app.route("/api/book_details", methods=["POST"])
def api_book_details():
    # get the details
    isbn = request.data.decode()
    print("In the book details api",isbn)
    book = Books.query.filter_by(isbn = isbn).first()
    reviews = Reviews.query.filter_by(book_isbn=isbn).all() 
    for i in reviews:
        print(i)
    print(reviews,len(reviews),type(reviews))
    print(book.title)
    if reviews == []:
        return jsonify({'title': book.title,
            'author':book.author,
            'isbn': book.isbn,
            'year':book.year,
            'reviews': 'null'
            })
    r = []
    for review in reviews:
        dic = {}
        dic['username'] = review.user_name
        dic['rating'] = review.rating
        dic['review'] = review.review
        r.append(dic)
    print(r)
    return jsonify({'title':book.title,
            'author':book.author,
            'isbn': book.isbn,
            'year': book.year,
            'reviews': r
            })

@app.route("/api/submit_review", methods=["POST"])
def api_submit_review():
    user = session.get("USERNAME")
    re = request.form.get('post-review-data')
    re1 = request.form.get('rating-value')
    isbn = request.form.get('isbn')
    print(re,re1,isbn,'here')
    if re == '' or re1=='0':
        return jsonify ({
            'success' : False,
            'user' : user,
            'statement':'Please complete the feedback or  Select a rating '
            })
    try:
        review = Reviews(book_isbn=isbn, user_name=user, rating=int(re1), review=re)
        db.session.add(review)
        db.session.commit()
        return jsonify({
            'success' : True,
            'user' : user,
            'statement':''
            })
    except Exception as e:
        print(str(e))
        return jsonify ({
            'success' : False,
            'user' : user,
            'statement':'Already Reviewed'
            })


if __name__ == "__main__":
    app.run(debug=True)
