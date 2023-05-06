from flask import Blueprint, render_template, request, flash, jsonify

views = Blueprint('views', __name__)

@views.route('/')
@views.route('/home')
def home():
    return render_template("home.html")

@views.route('/login')
def login():
    return render_template("login.html")