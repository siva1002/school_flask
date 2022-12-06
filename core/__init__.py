from flask import Flask, render_template, request
from flask_admin import Admin
from .extension import mongo
from . views import views
from flask_migrate import Migrate
from flask_alembic import Alembic


alembic = Alembic()


def create_app():
    app = Flask(__name__, template_folder='templates')
    # app.config['SQLALCHEMY_DATABASE_URI'] ='postgresql://postgres:root@localhost/school'
    app.config['MONGO_URI'] = 'mongodb://localhost:27017/accounts'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['DEBUG'] = True
    app.app_context().push()
    app.register_blueprint(views, url_prefix='/')
    alembic.init_app(app)
    mongo.init_app(app)
    # Migrate(app, db)
    return app
