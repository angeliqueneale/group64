from flask import Blueprint, flash, render_template, request, url_for, redirect
from flask_bcrypt import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user
from .models import User
from .forms import LoginForm, RegisterForm
from . import db

# Create a blueprint - make sure all BPs have unique names
auth_bp = Blueprint('auth', __name__)

# this is a hint for a login function
@auth_bp.route('/login', methods=['GET', 'POST'])
# view function
def login():
    login_form = LoginForm()
    error = None
    if login_form.validate_on_submit():
        username = login_form.username.data
        password = login_form.password.data
        user = db.session.scalar(db.select(User).where(User.username==username))
        if user is None:
            error = 'Incorrect user name'
        elif not check_password_hash(user.password_hash, password): # takes the hash and cleartext password
            error = 'Incorrect password'
        if error is None:
            login_user(user)
            nextp = request.args.get('next') # this gives the url from where the login page was accessed
            print(nextp)
            if nextp is None or not nextp.startswith('/'):
                return redirect(url_for('main.home'))
            return redirect(nextp)
        else:
            flash(error)
    return render_template('user.html', form=login_form, heading='Login')

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():  
  #create the form
    form = RegisterForm()
    #this line is called when the form - POST
    if form.validate_on_submit():
      print('Register form submitted')
       
      #get username, password and email from the form
      uname =form.username.data
      pwd = form.password.data
      email=form.email.data
      existing_user = User.query.filter_by(username=uname).first()
      if existing_user:
        flash('Username already exists. Please choose a different one.', 'danger')
        return render_template('register.html', form=form)  # Render the registration template with the form

      pwd_hash = generate_password_hash(pwd)
      #create a new user model object
      new_user = User(username=uname, password_hash=pwd_hash, email=email)
      db.session.add(new_user)
      db.session.commit()
     
      return redirect(url_for('auth.login'))
       
    return render_template('register.html', form=form, heading='Register')

@auth_bp.route('/logout')
def logout():
  logout_user()
  return render_template('logout.html')