import json

from flask_login import UserMixin

class Movie:
    def __init__(self, id: int, name: str, img: str):
        self.id = id
        self.name = name
        self.img = img

    def toJSON(self):
        return vars(self)

class User(UserMixin):
    def __init__(self, id: int, email: str, name: str, movies_id: list):
        self.id = id
        self.email = email
        self.name = name
        self.movies_id = movies_id
        self.movies = []

    def update_movies(self, movies: list):
        self.movies = movies
