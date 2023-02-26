from flask import Flask, render_template, redirect, session, flash
from flask_debugtoolbar import DebugToolbarExtension
from models import connect_db, db, User, Feedback
from forms import RegisterForm, LoginForm, FeedbackForm
from sqlalchemy.exc import IntegrityError


app = Flask(__name__)
app.app_context().push()
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///feedback_db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True
app.config["SECRET_KEY"] = "chamberofsecrets"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)

connect_db(app)
db.create_all()

@app.route('/')
def homepage():
  """Redirect user from homepage to register."""
  return redirect('/register')

@app.route('/register', methods=['GET', 'POST'])
def register_user():
  """Register user: produce form & handle form submission."""
  form = RegisterForm()
  
  #POST request
  if form.validate_on_submit():
      name = form.username.data
      pwd = form.password.data
      email = form.email.data
      first_name = form.first_name.data
      last_name = form.last_name.data

      new_user = User.register(name,pwd,email,first_name,last_name)
      db.session.add(new_user)
      try:
        db.session.commit()
      except IntegrityError:
        form.username.errors.append('Username taken. Please choose another.')
        return render_template('register.html', form=form)
      session['user'] = new_user.username
      flash(f'Welcome {new_user.username}! Successfully Created Your Account!', 'success')
      return redirect(f'/users/{new_user.username}')
  #GET request
  return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login_user():
  form = LoginForm()

  if form.validate_on_submit():
    username = form.username.data
    password = form.password.data

    user = User.authenticate(username, password)

    if user:
      flash(f'Welcome back, {user.username}!', 'primary')
      session['user'] = user.username 
      return redirect(f'/users/{user.username}')
    else:
      form.username.errors = ['Doublecheck username.']
      form.password.errors = ['Doublecheck password.']

  return render_template('login.html', form=form)

@app.route('/logout')
def logout_user():
  session.pop('user')
  flash('See you later!', 'info')
  return redirect('/')

###### User routes ######

@app.route('/users/<username>')
def show_user(username):
  """Show secret page to registered/logged in users."""
  user = User.query.get_or_404(username)
  if user.username not in session['user']: 
    flash('Please login first.', 'danger')
    return redirect('/')  
  return render_template('feedback/user.html', user=user )  
  
@app.route('/users/<username>/delete', methods=['POST'])
def delete_user(username):
  """Delete user and associated feedback."""
  user = User.query.get_or_404(username)
  if session['user'] == user.username:
    db.session.delete(user)
    db.session.commit()
    session.pop('user')
    flash(f'Account {user.username} deleted.', 'success')

  return redirect('/')

###### Feedback routes ######
@app.route('/users/<username>/feedback/add', methods=['GET','POST'])
def show_feedback_form(username):
  """Show feedback form and handle adding feedback."""
  form = FeedbackForm()
  user = User.query.get_or_404(username)
  if session['user'] == user.username:
    if form.validate_on_submit():
      title = form.title.data
      content = form.content.data
      new_feedback = Feedback(title=title, content=content, user=user.username)
      db.session.add(new_feedback)
      db.session.commit()
      flash('Feedback added!', 'success')
      return redirect(f'/users/{user.username}')
    
  return render_template('feedback/add.html', form=form, user=user)

@app.route('/feedback/<int:id>/update', methods=['GET','POST'])
def edit_feedback_form(id):
  """Show edit feedback form and handle edits."""
  feedback = Feedback.query.get_or_404(id)
  edit_form = FeedbackForm(obj=feedback)
  if session['user'] == feedback.users.username:
    if edit_form.validate_on_submit():
      feedback.title = edit_form.title.data
      feedback.content = edit_form.content.data
      db.session.add(feedback)
      db.session.commit()
      flash(f'Feedback saved!', 'success')
      return redirect(f'/users/{feedback.users.username}')

  return render_template('feedback/edit.html', form=edit_form, feedback=feedback)

@app.route('/feedback/<int:id>/delete', methods=['POST'])
def delete_feedback(id):
  """Delete a single feedback."""
  feedback = Feedback.query.get_or_404(id)
  if session['user'] == feedback.users.username:
    db.session.delete(feedback)
    db.session.commit()
    flash(f'Feedback deleted.', 'success')
    return redirect(f'/users/{feedback.users.username}')

