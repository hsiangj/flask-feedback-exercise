from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, PasswordField
from wtforms.validators import InputRequired, Optional

class RegisterForm(FlaskForm):
    """Form for registering a user."""

    username = StringField("Username", validators=[InputRequired(message="Username can't be blank")])
    password = PasswordField("Password", validators=[InputRequired(message="Password can't be blank")])
    email = StringField("Email", validators=[InputRequired(message="Please enter an email")])
    first_name = StringField("First Name", validators=[InputRequired(message="Please enter a first name")])
    last_name = StringField("Last Name", validators=[InputRequired(message="Please enter a last name")])

class LoginForm(FlaskForm):
    """Form for user to login."""

    username = StringField("Username", validators=[InputRequired(message="Username can't be blank")])
    password = PasswordField("Password", validators=[InputRequired(message="Password can't be blank")])

class FeedbackForm(FlaskForm):
    """Form for adding feedback."""

    title = StringField("Title", validators=[Optional()])
    content = TextAreaField("Content", validators=[Optional()])