import json
from urllib.request import urlopen

from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_user, login_required, logout_user, current_user

views = Blueprint('views', __name__)

API_LINK = 'http://www.omdbapi.com/?apikey=8fa3bc0c&t='

@views.route('/')
@views.route('/home')
@login_required
def home():
    return render_template("home.html", user=current_user)

@views.route('/movie')
@login_required
def movie():
    return render_template("movie.html", user=current_user, movie_title="placeholder")

@views.route('/receive_data', methods=["POST"])
def receive_data():
    data = request.get_json()  # Get the JSON data sent from the client
    received_data = data.get('dataFromJS')  # Access the specific data field
    print(received_data)

    response = urlopen(API_LINK + received_data)
    data_json = json.loads(response.read())
    return data_json