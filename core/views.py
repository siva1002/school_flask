from .models import User,Profile,Token
import uuid
from . serializer import UserSerializer
from mongoengine import connect,get_db
connect(host='mongodb+srv://root:12345@cluster0.kv3gwol.mongodb.net/school')
db=get_db()
from flask import Blueprint, render_template, request,Response
from bson.json_util import dumps
from flask_login import login_user
views = Blueprint('views', __name__)


@views.route('/')
def userdetails():
    pipeline=[{"$lookup":{
  "from": "profile",
  "localField": "_id",
  "foreignField": 'user',
  "as": 'profile'
}}]
    user=db.user.aggregate(pipeline=pipeline)
    query=list(user)
    data=dumps(query)
    return data


@views.route('login/', methods=['POST'])
def login():
    data = request.get_json()
    user = User.objects(email=data['email'], phone=data['phone']).first()
    token = (Token.objects(user_id=user)).first()
    login_user(user=user, remember=True)
    if not token:
        token = Token(user_id=user)
        token.save()
    return {'status': user.to_json(),'token':token.token_id}

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
@views.route('user/<id>',methods=['GET'])
def user(id):
    user=User.objects.get(pk=id)
    return user.to_json()