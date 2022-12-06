from flask import Flask, render_template, request
from flask_admin import Admin
from .extension import mongo
from . views import views
from flask_migrate import Migrate
from flask_alembic import Alembic
from flask_jwt_extended import JWTManager
from datetime import timedelta

alembic = Alembic()
jwt = JWTManager()
db = None


def create_app():
    app = Flask(__name__, template_folder='templates')
    # app.config['SQLALCHEMY_DATABASE_URI'] ='postgresql://postgres:root@localhost/school'
    app.config['MONGO_URI'] = 'mongodb+srv://root:YmaXmz16j8AfLi94@cluster1.lcpgfzf.mongodb.net/schooldb'
    # app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['DEBUG'] = True
    app.app_context().push()
    app.register_blueprint(views, url_prefix='/')
    # alembic.init_app(app)
    mongo.init_app(app)
    print(mongo)
    # db = mongo.db['scholldb']
    jwt.init_app(app)
    app.config['JSW_ACCESS_TOKEN_EXPIRES'] = timedelta(days=1)
    # Migrate(app, db)
    return app
