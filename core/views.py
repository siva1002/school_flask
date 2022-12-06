from .models import User, PydanticObjectId
import uuid
from . serializer import UserSerializer
from .extension import mongo
# from . import app
# from .models import User, Profile,Token
from flask import Blueprint, render_template, request, jsonify, make_response
import jwt
import json
from .models import JSONEncoder

views = Blueprint('views', __name__)


@views.route('/')
def index():

    return 'Hello, world'


@views.route('login/', methods=['POST'])
def login():
    users = mongo.db.users
    data = request.json
    print(data)
    user = users.find_one({'email': data['email'], 'phone': data['phone']})
    user = json.dumps(user, cls=JSONEncoder)
    return user


@views.route('signup/', methods=['POST'])
def signup():
    users = mongo.db.users
    data = request.json
    # users.insert_one({'email': data['email'],
    #                   'phone': data['phone']})

    cocktail = User(**data)
    insert_result = users.insert_one(cocktail.to_bson())
    return 'created'
