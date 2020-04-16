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
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    register_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
