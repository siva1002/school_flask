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
from flask_jwt_extended import JWTManager
from flask_cors import CORS
import datetime

db = None
login_manager = LoginManager()
login_manager.login_view = 'views.login'


@login_manager.user_loader
def create_app():
    app = Flask(__name__, template_folder='templates')
    app.config['MONGO_URI'] = 'mongodb+srv://root:YmaXmz16j8AfLi94@cluster1.lcpgfzf.mongodb.net/schooldb'
    app.config['SECRET_KEY'] = 'thisiskey'
    app.config['JWT_SECRET_KEY'] = 'thisisjwtkey'
    # app.config['JWT_TOKEN_LOCATION'] = 'cookies'
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = datetime.timedelta(days=1)
    app.config['DEBUG'] = True
    app.app_context().push()
    # mongo.init_app(app)
    # print(mongo)
    connect(
        host='mongodb+srv://root:YmaXmz16j8AfLi94@cluster1.lcpgfzf.mongodb.net/schooldb'
    )
    app.register_blueprint(views, url_prefix='/')
    login_manager.init_app(app)
    app.config["SESSION_PERMANENT"] = False
    app.config["SESSION_TYPE"] = "filesystem"
    JWTManager(app)
    CORS(app)
    # session.init_app(app)
    return app
