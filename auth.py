from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, User

auth = Blueprint('auth',__name__)  #creating or initializing blueprint and naming(as auth) it.


#SignUp
@auth.route('/signup',methods = ['GET','POST'])
def signup():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        role = request.form.get('role')

        user_exists = User.query.filter_by(username=username).first()   #if the user has already signed up
        if user_exists:
            flash('Username already exists', 'danger')
            return redirect(url_for('auth.signup'))   #Backend validation
        
        hashed_password = generate_password_hash(password)

        new_user = User(username = username, password=hashed_password, role = role)
        db.session.add(new_user)
        db.session.commit()

        flash('Account created successfully! Please log in', 'success')
        return redirect(url_for('auth.login'))
    return render_template('signup.html')

#login
@auth.route('/login',methods = ['GET','POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = User.query.filter_by(username = username).first()

        if user and check_password_hash(user.password, password):
            login_user(user)
            flash('Logged in successfully', 'success')
            return redirect(url_for('views.dashboard'))
        
        flash('Invalid Credentials. Please try again','danger')
    return render_template('login.html')

#logout
@login_required
@auth.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('auth.login'))
