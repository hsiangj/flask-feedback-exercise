from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def connect_db(app):
    """Connect this model to Flask app. Function called in app.py"""
    db.app = app
    db.init_app(app)

class User(db.Model):
    """User Model for user login info"""

    __tablename__ = 'users'

    username = db.Column(db.String(20), unique=True, primary_key=True)
    password = db.Column(db.Text, nullable=False)
    email = db.Column(db.String(50), nullable=False, unique=True)
    first_name = db.Column(db.String(30), nullable=False)
    last_name = db.Column(db.String(30), nullable=False)