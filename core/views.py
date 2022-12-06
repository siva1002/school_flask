from .models import User,Profile
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
    users = mongo.db.users
    data = request.json
    print(data)
    user = users.find_one({'email': data['email'], 'phone': data['phone']})
    return user


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
