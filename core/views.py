from .models import User, Token
import uuid
from . serializer import UserSerializer
from .extension import mongo
# from . import app
# from .models import User, Profile,Token
from flask import Blueprint, render_template, request, jsonify, make_response
import jwt
import json
# from .models import JSONEncoder
from flask_login import login_user
views = Blueprint('views', __name__)


@views.route('/')
def index():

    return 'Hello, world'


@views.route('login/', methods=['POST'])
def login():
    data = request.json
    user = User.objects(email=data['email'], phone=data['phone']).first()
    token = (Token.objects(user_id=user)).first()
    login_user(user=user, remember=True)
    if not token:
        token = Token(user_id=user)
        token.save()
    return {'status': user.to_json()}


@views.route('signup/', methods=['POST'])
def signup():
    data = request.json
    user = User(email=data['email'], phone=data['phone'])
    print(user)
    user.save()
    return 'created'
