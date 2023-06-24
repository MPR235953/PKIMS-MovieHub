import json
from urllib.request import urlopen

from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_user, login_required, logout_user, current_user

from src.website import cursor, connection

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
    # Generate the column names and values for the SQL query
    del data["Ratings"]

    columns = ', '.join(data.keys())
    values = ', '.join(['%s'] * len(data))

    # Create the SQL query
    query = f"INSERT INTO movies ({columns}) VALUES ({values})"

    # Execute the query with the dictionary values
    cursor.execute(query, list(data.values()))

    # Commit the changes to the database
    connection.commit()

    #insert = "insert into movies (Title, Year, Rated, Released, Runtime, Genre, Director, Writer, Actors, Plot, Language, Country, Awards, Poster, Metascore, imdbRating, imdbVotes, imdbID, Type, DVD, BoxOffice, Production, Website, Response) VALUES ('{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}')".format(data["Title"], data["Year"], data["Rated"], data["Released"], data["Runtime"], ','.join(data["Genre"]), data["Director"], data["Writer"], data["Actors"], data["Plot"], data["Language"], data["Country"], data["Awards"], data["Poster"], data["Metascore"], data["imdbRating"], data["imdbVotes"], data["imdbID"], data["Type"], data["DVD"], data["BoxOffice"], data["Production"], data["Website"], data["Response"])
    #cursor.execute(insert, data)
    #connection.commit()