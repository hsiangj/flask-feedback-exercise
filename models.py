from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

db = SQLAlchemy()
bcrypt = Bcrypt()

def connect_db(app):
    """Connect this model to Flask app. Function called in app.py"""
    db.app = app
    db.init_app(app)

class User(db.Model):
    """User Model for site user"""

    __tablename__ = "users"

    username = db.Column(db.String(20), unique=True, primary_key=True)
    password = db.Column(db.Text, nullable=False)
    email = db.Column(db.String(50), nullable=False, unique=True)
    first_name = db.Column(db.String(30), nullable=False)
    last_name = db.Column(db.String(30), nullable=False)

    feedbacks = db.relationship("Feedback", backref="users", cascade="all, delete-orphan")

    @classmethod
    def register(cls, username, pwd, email, first, last):
        """Register user w/hashed password & return user."""

        hashed = bcrypt.generate_password_hash(pwd)
        # turn bytestring into normal (unicode utf8) string
        hashed_utf8 = hashed.decode('utf8')

        return cls(username=username, password=hashed_utf8, email=email, first_name=first, last_name=last)
    
    @classmethod
    def authenticate(cls, username, pwd):
        """Validate that user exists & password is correct.

        Return user if valid; else return False.
        """
        user = User.query.filter_by(username=username).first()
        #If there is a user and check pw hash
        if user and bcrypt.check_password_hash(user.password, pwd):
            #return user instance
            return user
        else:
            return False
        
class Feedback(db.Model):
    """Feedback Model for user feedback"""

    __tablename__ = "feedback"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    user = db.Column(db.Text, db.ForeignKey("users.username"), nullable=False)

    
    

