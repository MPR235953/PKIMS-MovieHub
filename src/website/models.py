from flask_login import UserMixin

class User(UserMixin):
    def __init__(self, id, email, name, movies_id):
        self.id = id
        self.email = email
        self.name = name
        self.movies_id = movies_id

    def get_id(self):
        return str(self.id)


class Movie:
    def __init__(self):
        pass
