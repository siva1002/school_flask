from .models import User, Profile, Token
from mongoengine import connect, get_db
from bson.json_util import dumps
from . serializer import UserSerializer
import uuid
from .extension import mongo
from .models import User, Token
from flask import Blueprint, render_template, request, jsonify, make_response, Response
from functools import wraps
from flask import session
views = Blueprint('views', __name__)
connect(
    host='mongodb+srv://root:YmaXmz16j8AfLi94@cluster1.lcpgfzf.mongodb.net/schooldb'
)
db = get_db()


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


@views.route('/')
def userdetails():
    pipeline = [{"$lookup": {
        "from": "profile",
        "localField": "_id",
        "foreignField": 'user',
        "as": 'profile'
    }}]
    user = User.objects.aggregate(pipeline=pipeline)
    query = list(user)
    data = dumps(query)
    return data


@views.route('login/', methods=['POST'])
def login():
    data = request.get_json()
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


@views.route('signup/<int:id>', methods=['POST'])
def signup():
    data = request.json
    user = User(email=data['email'], phone=data['phone'])
    print(user)
    user.save()
    return {'user': user}
    # try:
    #     print(request.json)
    #     data = request.json
    #     user = User(email=data['email'], phone=data['phone'],
    #                 registernumber=data['registernumber'])
    #     user.save()
    #     profile = Profile(fullname=data['fullname'], firstname=data["firstname"],
    #                       lastname=data['lastname'], address=data['address'], usertype=data['usertype'], user=user)
    #     profile.save()
    #     return Response(dumps({'message': 'created'}), status=200)
    # except Exception as e:
    #     print(e)
    #     return Response(dumps({'message': 'not created'}),status=400)


@views.route('logout')
@token_required
def logout():
    session['token'] = None
    session['user'] = None
    return {'status': 'logged out'}


@views.route('user/<id>', methods=['GET', 'PATCH'])
@token_required
def user(id):
    pipeline = [{'$match': {'_id': int(id)}}, {"$lookup": {
        "from": "profile",
        "localField": "_id",
        "foreignField": 'user',
        "as": 'profile'
    }}]
    if request.method != 'PATCH':
        try:
            user = User.objects.aggregate(pipeline=pipeline)
            print(user)
            data = dumps(user)
            print(data)
            if user:
                return Response(dumps({'data': data}), status=200)
        except Exception as e:
            print(e)
            return Response(dumps({'message': e}), status=400)
    try:
        user = db.user.aggregate(pipeline=pipeline)
        if user:
            return Response({'data': data}, status=200)
    except Exception as e:
        return Response(dumps({'message': e}), status=400)
