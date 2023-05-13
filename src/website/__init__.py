from flask import Flask
from pymongo import MongoClient

#clent = MongoClient('127.0.0.1', 27017, username='root', password='root')
client = MongoClient('mongodb://root:root@pkims-moviehub-mongo-container-1')
db = client['user-data']
collection = db['users']

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'secret key'

    from .views import views
    from .auth import auth
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    return app