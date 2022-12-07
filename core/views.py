from .models import User, Token
from .extension import mongo
from .models import User, Token
from flask import Blueprint, render_template, request, jsonify, make_response
from functools import wraps
from flask import session
views = Blueprint('views', __name__)


def token_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session['token']:
            token_id = session['token']
            print(token_id)
        else:
            token_id = ((request.headers['Authorization']).split(' '))[-1]
        token = Token.objects(token_id=token_id)
        if not token:
            return {'data': 'invalid token'}
        user = token[0].user_id
        return f(*args, **kwargs)
    return decorated_function


@views.route('login/', methods=['POST'])
def login():
    data = request.json
    user = User.objects(email=data['email'], phone=data['phone']).first()
    token = (Token.objects(user_id=user)).first()
    session["token"] = token.token_id
    print(session['token'])
    if not token:
        token = Token(user_id=user)
        token.save()
    print(request.headers)
    return {'status': user.to_json(), 'token': token.token_id}


@views.route('/')
@token_required
def index():
    return 'Hello, world'


@views.route('signup/', methods=['POST'])
def signup():
    data = request.json
    user = User(email=data['email'], phone=data['phone'])
    print(user)
    user.save()
    return {'user': user}


@views.route('logout')
@token_required
def logout():
    session['token'] = None
    session['user'] = None
    return {'status': 'logged out'}
