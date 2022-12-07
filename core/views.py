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
    host='mongodb+srv://root:12345@cluster0.kv3gwol.mongodb.net/school'
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
@token_required
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


@views.route('signup/', methods=['POST'])
def signup():
    try:
        print(request.json)
        data= request.json
    
        user=User(email=data['email'],phone=data['phone'],registernumber=data['registernumber'])
        user.save()
        profile=Profile(fullname=data['fullname'],firstname=data["firstname"],lastname=data['lastname'],address=data['address'],usertype=data['usertype'],user=user)
        profile.save()
        return Response(dumps({'message':'created'}),status=200)
    except Exception as e:
        print(e)
        return Response(dumps({'message':'not created'}),status=400)
@views.route('user/<id>',methods=['GET','PATCH'])
def user(id):
    pipeline = [{'$match': {'_id': int(id)}}, {"$lookup": {
        "from": "profile",
        "localField": "_id",
        "foreignField": 'user',
        "as": 'profile'
    }}]
    if request.method != 'PATCH':
        try:
            user=list(User.objects.aggregate(pipeline=pipeline))
            data=dumps(user)
            if user :
                return Response(dumps({'data':data}),status=200)
            return Response(dumps({'message':'User doesnt Existed'}),status=400)
        except Exception as e:
            print(e)
            return Response(dumps({'message': e}), status=400)
    try:
        user=User.objects(id=int(id))
        data=request.json
        print(data)
        user.update(email=data['email'],phone=data['phone'],registernumber=data['registernumber'])
        profile=Profile.objects(user=int(id))
        profile.update(fullname=data['fullname'],firstname=data["firstname"],lastname=data['lastname'],address=data['address'],usertype=data['usertype'])
        return Response(dumps({'data':'Working with patch method'}),status=200)
    except Exception as e:
        return Response(dumps({'message': e}), status=400)
