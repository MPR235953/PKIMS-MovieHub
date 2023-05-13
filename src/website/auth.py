from flask import Blueprint, render_template, request, flash

auth = Blueprint('auth', __name__)

@auth.route("/login", methods=['GET', 'POST'])
def login():
    data = request.form
    return render_template("login.html")

@auth.route("/logout")
def logout():
    return "logout"

@auth.route("/sign_up", methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        first_name = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        if len(email) < 4:
            flash('Email is too short, must be at least 4 characters', category='alert-danger')
        elif len(first_name) < 2:
            flash('First name is too short, must be at least 2 characters', category='alert-danger')
        elif password1 != password2:
            flash('Difference between passwords', category='alert-danger')
        elif len(password1) < 7:
            flash('Password is too short, must be at least 7 characters', category='alert-danger')
        else:
            flash('Account created!', category='alert-success')
    return render_template("sign_up.html")