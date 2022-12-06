from .models import User
from flask import Flask, render_template, request
from flask_admin import Admin
from .extension import mongo
from . views import views
from flask_migrate import Migrate
from flask_alembic import Alembic
from flask_jwt_extended import JWTManager
from datetime import timedelta
from mongoengine import connect
from flask_login import LoginManager
# alembic = Alembic()


db = None
login_manager = LoginManager()
login_manager.login_view = 'views.login'


@login_manager.user_loader
def create_app():
    app = Flask(__name__, template_folder='templates')
    # app.config['SQLALCHEMY_DATABASE_URI'] ='postgresql://postgres:root@localhost/school'
    app.config['MONGO_URI'] = 'mongodb+srv://root:12345@cluster0.kv3gwol.mongodb.net/school'
    app.config['SECRET_KEY'] = 'this is token'
    # app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['DEBUG'] = True
    app.app_context().push()
    # mongo.init_app(app)
    # print(mongo)
    connect(
        host='mongodb+srv://root:12345@cluster0.kv3gwol.mongodb.net/school'
    )
    app.register_blueprint(views, url_prefix='/')
    login_manager.init_app(app)
    return app
