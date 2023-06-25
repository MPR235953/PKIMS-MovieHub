import json
from urllib.request import urlopen

from flask import Blueprint, render_template, request, flash, jsonify, session
from flask_login import login_user, login_required, logout_user, current_user

from src.website import cursor, connection, collection
from src.website.models import Movie

views = Blueprint('views', __name__)

API_LINK = 'http://www.omdbapi.com/?apikey=8fa3bc0c&t='

@views.route('/')
@views.route('/home')
@login_required
def home():
    movies = session.get("movies")
    current_user.update_movies(movies)
    return render_template("home.html", user=current_user)

@views.route('/movie')
@login_required
def movie():
    return render_template("movie.html", user=current_user, movie_title="placeholder")

@views.route('/receive_data', methods=["POST"])
def receive_data():
    data = request.get_json()
    received_data = data.get('dataFromJS')
    print(received_data)

    rows, columns = get_movie_by_name(received_data)
    if not rows:
        response = urlopen(API_LINK + received_data)
        data_json = json.loads(response.read())
        if "Error" in data_json.keys(): return Exception
        data_json["Title"] = received_data
        insert_movie(data_json)
        return data_json
    else:
        data = []
        for row in rows:
            data.append(dict(zip(columns, row)))
        data_json = json.dumps(data[0], indent=4)
        return data_json


def get_movie_by_name(movie_title: str):
    query = f"select * from movies where Title = '{movie_title}' limit 1"
    cursor.execute(query)
    rows = cursor.fetchall()
    columns = [desc[0] for desc in cursor.description]
    return rows, columns

def insert_movie(data: dict):
    del data["Ratings"]
    columns = ', '.join(data.keys())
    values = ', '.join(['%s'] * len(data))
    query = f"INSERT INTO movies ({columns}) VALUES ({values})"
    cursor.execute(query, list(data.values()))
    connection.commit()

@views.route('add_movie_to_user', methods=["POST"])
def add_movie_to_user():
    try:
        data = request.get_json()
        received_data = data.get('dataFromJS')
        print(received_data)

        query = f"select id, Title, Poster from movies where Title = '{received_data}' limit 1"
        cursor.execute(query)
        rows = cursor.fetchall()
        id, name, poster = 0, "", ""
        for row in rows:
            id = row[0]
            name = row[1]
            poster = row[2]

        if collection.find_one({"_id": current_user.id, "moviesId": id}):
            flash('Movie already added', category='alert-warning')
        else:
            collection.update_one(
                {"_id": current_user.id},
                {"$addToSet": {"moviesId": int(id)}}
            )
            current_user.movies_id.append(int(id))
            current_user.add_movie(Movie(int(id), name, poster))
            current_user.save()
            flash('Movie was added', category='alert-success')
        return {"Error": False}
    except Exception:
        flash('Movie cannot be added', category='alert-danger')
        return {"Error": True}
