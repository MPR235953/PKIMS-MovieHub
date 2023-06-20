from bson import ObjectId
from flask import Flask
from flask_login import LoginManager
from pymongo import MongoClient
from src.website.models import User
import mysql.connector

client = MongoClient('mongodb://root:root@pkims-moviehub-mongo-container-1', maxIdleTimeMS=60000, serverSelectionTimeoutMS=5000)
db = client['user_db']
collection = db['users']

connection = mysql.connector.connect(
    host='pkims-moviehub-mysql-container-1',
    user='root',
    password='root',
    database='movie_db'
)
cursor = connection.cursor()

query = "SELECT * FROM movies"
cursor.execute(query)

# Fetch all rows from the result
result = cursor.fetchall()

# Process the result
for row in result:
    print(row)


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'secret key'

    from .views import views
    from .auth import auth
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'  # where flask should redirect if we not logged
    login_manager.login_message_category = "alert-warning"
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        user = collection.find_one({'_id': ObjectId(user_id)})
        if not user:
            return None
        return User(user['_id'])

    return app