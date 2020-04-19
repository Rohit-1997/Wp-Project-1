"""
    This file is used to build models for
    out database
"""

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

# creating the user model
class User(db.Model):
    __tablename__ = "users_table"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    register_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)


# Creating the books model
class Books(db.Model):
    __tablename__ = "books"
    isbn = db.Column(db.String(50), primary_key=True, nullable=False)
    title = db.Column(db.String(200), nullable=False)
    author = db.Column(db.String(150), nullable=False)
    year = db.Column(db.Integer, nullable=False)
