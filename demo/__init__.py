from flask import Flask, render_template, request

from .extension import db
from . views import views
from flask_migrate import Migrate
from flask_alembic import Alembic

alembic = Alembic()


def create_app():
    app = Flask(__name__, template_folder='templates')
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://abd:root@localhost/schoolflask'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['DEBUG'] = True
    app.app_context().push()
    app.register_blueprint(views, url_prefix='/')
    db.init_app(app)
    alembic.init_app(app)
    Migrate(app, db)
    return app
