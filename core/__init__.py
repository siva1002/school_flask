from .models import User
from flask import Flask, render_template, request
from flask_admin import Admin
# from .extension import mongo
from .accounts import accounts
from .academics import academics
from flask_cors import CORS
import datetime
# from flask_rest_paginate import Pagination

db = None
pagination = None


def create_app():
    app = Flask(__name__, template_folder='templates')
    app.config['MONGO_URI'] = 'mongodb+srv://root:YmaXmz16j8AfLi94@cluster1.lcpgfzf.mongodb.net/schooldb'
    app.config['SECRET_KEY'] = 'thisiskey'
    # app.config['JWT_SECRET_KEY'] = 'thisisjwtkey'
    # app.config['JWT_TOKEN_LOCATION'] = 'cookies'
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = datetime.timedelta(days=1)
    app.config['DEBUG'] = True
    app.app_context().push()
    # mongo.init_app(app)
    # print(mongo)
    app.register_blueprint(accounts, url_prefix='/')
    # db = accounts.db
    app.register_blueprint(academics, url_prefix='/')
    app.config["SESSION_PERMANENT"] = False
    app.config["SESSION_TYPE"] = "filesystem"
    CORS(app)
    # session.init_app(app)
    return app
