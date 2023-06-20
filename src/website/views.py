from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_user, login_required, logout_user, current_user

views = Blueprint('views', __name__)

@views.route('/')
@views.route('/home')
@login_required
def home():
    return render_template("home.html", user=current_user)

@views.route('/movie')
@login_required
def movie():
    return render_template("movie.html", user=current_user)
