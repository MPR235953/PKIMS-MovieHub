from flask import Blueprint, render_template, request, flash, redirect, url_for
from pymongo.errors import ServerSelectionTimeoutError
from . import collection, User
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint('auth', __name__)

@auth.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        try:
            user = collection.find_one({"email": email})
            if user:
                if check_password_hash(user['password'], password):
                    flash('Logged successfully!', category='alert-success')
                    login_user(User(user['_id']), remember=True)  # store user in flask session
                    return redirect(url_for('views.home'))
                else:
                    flash('Incorrect password, try again', category='alert-danger')
            else:
                flash('Email does not exist', category='alert-danger')
        except ServerSelectionTimeoutError:
            flash('Connection timed out', category='alert-warning')

    return render_template("login.html", user=current_user)

@auth.route("/logout")
@login_required
def logout():
    logout_user()   # logout current user
    return redirect(url_for('auth.login'))

@auth.route("/sign_up", methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        first_name = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        try:
            user = collection.find_one({"email": email})

            if user:
                flash('Email already exist', category='alert-danger')
            elif len(email) < 4:
                flash('Email is too short, must be at least 4 characters', category='alert-danger')
            elif len(first_name) < 2:
                flash('First name is too short, must be at least 2 characters', category='alert-danger')
            elif password1 != password2:
                flash('Difference between passwords', category='alert-danger')
            elif len(password1) < 7:
                flash('Password is too short, must be at least 7 characters', category='alert-danger')
            else:
                collection.insert_one({'email': email, 'firstName': first_name, 'password': generate_password_hash(password1, method='sha256')})
                login_user(User(user['_id']), remember=True)  # store user in flask session
                flash('Account created!', category='alert-success')
                return redirect(url_for('views.home'))
        except ServerSelectionTimeoutError:
            flash('Connection timed out', category='alert-warning')

    return render_template("sign_up.html", user=current_user)