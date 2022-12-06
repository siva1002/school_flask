from .models import User,Profile,Token
import uuid
from . serializer import UserSerializer
from .extension import mongo
from mongoengine import connect
connect(host='mongodb+srv://root:12345@cluster0.kv3gwol.mongodb.net/school')
# from . import app
# from .models import User, Profile,Token
from flask import Blueprint, render_template, request, jsonify, make_response,Response
from bson.json_util import dumps
# from .models import JSONEncoder
from flask_login import login_user
views = Blueprint('views', __name__)


@views.route('/')
def index():
    pipeline=[{"$lookup":{
  "from": "profile",
  "localField": "_id",
  "foreignField": 'user',
  "as": 'profile'
}}]
    user=mongo.db.users.aggregate(pipeline=pipeline)
    query=list(user)
    data=dumps(query)
    print(data)
    return data


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
    try:
        data= request.get_json()
        user=User(email=data['email'],phone=data['phone'],registernumber=data['registernumber'])
        user.save()
        profile=Profile(fullname=data['fullname'],firstname=data["firstname"],lastname=data['lastname'],address=data['address'],usertype=data['usertype'],user=user)
        profile.save()
        return Response(dumps({'message':'created'}),status=200)
    except Exception as e:
        return Response(dumps({'message':e}),status=400)
