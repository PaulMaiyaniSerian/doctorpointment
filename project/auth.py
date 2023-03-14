from flask import Blueprint,flash, render_template, redirect, url_for, request
from . import db

from werkzeug.security import generate_password_hash, check_password_hash
from .models import User, Patient, Doctor
from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint('auth', __name__)

@auth.route('/auth/user/login')
def login():
    return render_template('login.html')

@auth.route('/auth/user/login', methods=['POST'])
def login_post():
    # login code goes here
    email = request.form.get('email')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False

    user = User.query.filter_by(email=email).first()


    if not user or not check_password_hash(user.password, password):
        flash('Please check your login details and try again.')
        return redirect(url_for('auth.login'))


    login_user(user, remember=False)
    return redirect(url_for('main.index'))

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))


@auth.route('/auth/user/register')
def signup():
    return render_template('register.html')


@auth.route('/auth/user/register', methods=['POST'])
# @login_required
def signup_post():
    email = request.form.get('email')
    first_name = request.form.get('first_name')
    last_name = request.form.get('last_name')
    # name = first_name + " " + last_name
    password = request.form.get('password')

    # code to validate and add user to database goes here
    # if not current_user.is_system_user:
    #     flash("you are not allowed to view this page")
    #     return redirect(url_for('main.index'))
    # check if there are any users
    # then the first becomes system_user
    users = User.query.filter_by()

    if users.count() < 1:
        print("creating admin account")
        admin_email = "admin@gmail.com"
        # admin_name = "admin"
        admin_password = "1234"
        admin_user = User(email=admin_email,is_system_user=True,first_name=first_name, last_name=last_name, password=generate_password_hash(admin_password, method='sha256'))

        # add the new user to the database
        db.session.add(admin_user)
        db.session.commit()
        logout_user()


   

    # print(name, '----------------------')

    user = User.query.filter_by(email=email).first() # if this returns a user, then the email already exists in database

    if user: # if a user is found, we want to redirect back to signup page so user can try again
        flash('Email address already exists')
        return redirect(url_for('auth.signup'))

    # create a new user with the form data. Hash the password so the plaintext version isn't saved.
    new_user = User(email=email, password=generate_password_hash(password, method='sha256'), first_name=first_name, last_name=last_name)
    

    # add the new user to the database
    db.session.add(new_user)
    db.session.commit()

    # create patiient profilre here
    new_patient = Patient(user=new_user.id)
    db.session.add(new_patient)
    db.session.commit()

    print(new_patient)
   
    return redirect(url_for('auth.login'))


@auth.route('/profile')
@login_required
def profile():
    doctor = Doctor.query.filter_by(user=current_user.id).first() 
    if doctor:
        return render_template('profile.html', user=current_user, doctor=doctor, patient=None)
    patient = Patient.query.filter_by(user=current_user.id).first()
    if patient:
        return render_template('profile.html', user=current_user, doctor=doctor, patient=None)
    
    else:
        return render_template('profile.html', user=current_user, doctor=None, patient=None)
