from flask import Flask
from flask_login import LoginManager
from pymongo import MongoClient

client = MongoClient('mongodb://root:root@pkims-moviehub-mongo-container-1', maxIdleTimeMS=60000, serverSelectionTimeoutMS=5000)
db = client['user-data']
collection = db['users']

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'secret key'

    from .views import views
    from .auth import auth
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'  # where flask should redirect if we not logged
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return collection.find_one({"_id": id})

    return app