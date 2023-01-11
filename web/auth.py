from flask import Blueprint,render_template,request,flash,redirect,url_for
from .models import User
from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_required, login_user, logout_user, current_user
from .crypto import generate

auth = Blueprint('auth', __name__)

#Route to login page/first screen
@auth.route('/login', methods=['GET', 'POST'])
def login():
    #Check data request method, if 'POST' proceed with login procedure, else render page.
    if request.method == 'POST':
        #initialize variables from formdata
        email=request.form.get('email')
        password = request.form.get('password')

        #define user variable based on his email and check 
        # if the entered password produces the same hash value as the database entry
        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in successfully!', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password, try again!', category='error')
        else:
            flash('Email does not exist', category='error')

    return render_template("login.html", user=current_user)

#Route to exit from user profile, uses built in functions
@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

#Route to user registration form
@auth.route('/sign-up', methods=['GET', 'POST'])
def signUp():
    #Check data request method, if 'POST' proceed with registration, else render page.
    if request.method == 'POST':
        #Initialize user variables based on html formdata
        email = request.form.get('email')
        firstName = request.form.get('firstName')
        lastName = request.form.get('lastName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        
        #Define user variable based on DB query and check if user exists
        user = User.query.filter_by(email=email).first()

        if user:
            flash('Email already exists!', category='error')
        #Do some data integrity and policy checks
        if len(email) < 4:
            flash('Email must be at least 4 characters', category='error')
        elif len(firstName) == 0 or len(lastName) == 0 or len(password1) == 0:
            flash('All fields must be filled!', category='error')
        elif password1 != password2:
            flash('Passwords don\'t match!', category='error')
        else:
            #Generate a cryptographic key that can be used for data encryption
            passKey = generate(password1)
            #Create User object and insert entry into database
            newUser = User(
                email = email, 
                firstName = firstName, 
                lastName = lastName, 
                passKey = passKey, 
                #Hash password before database insertion so it can be stored safely 
                password = generate_password_hash(password1, method='sha256')
                )
            db.session.add(newUser)
            db.session.commit()
            login_user(newUser, remember=True)
            flash('Account created!', category='success')
            return redirect(url_for('views.home'))

    return render_template("signup.html", user=current_user)