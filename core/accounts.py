from .models import User, Profile, Token
from mongoengine import connect, get_db
from bson.json_util import dumps, loads
from .extension import mongo
from .models import User, Token, Grade
from flask import Blueprint, render_template, request, jsonify, make_response, Response
from functools import wraps
from .utils import token_required
from flask import session
accounts = Blueprint('accounts', __name__)

# db connection
connect(
    host='mongodb+srv://root:12345@cluster0.kv3gwol.mongodb.net/school'
)
db = get_db()

pipeline = [{"$lookup": {
    "from": "profile",
    "localField": "_id",
    "foreignField": 'user',
    "as": 'profile'
}}]

# user details


@accounts.route('/')
def userdetails():
    user = loads(session['user'])
    print(user['user_type'])
    user_pipeline = pipeline
    if user['user_type'] == 'is_admin':
        queryset = User.objects.aggregate(pipeline=user_pipeline)
    elif user['user_type'] == 'is_staff':
        user_pipeline.insert(
            0, {'$match': {'user_type': 'is_student'}})
        queryset = User.objects.aggregate(
            pipeline=user_pipeline)
    else:
        user_pipeline.insert(
            0, {'$match': {'_id': int(user['_id'])}})
        queryset = User.objects.aggregate(
            pipeline=user_pipeline)
    queryset = dumps(queryset)
    return {'status': 'success', 'data': queryset}

# login


@accounts.route('login/', methods=['POST'])
def login():
    data = request.get_json()
    user = User.objects(email=data['email'], phone=data['phone'])[0]
    if not user:
        return Response(dumps({'message': "User doesn't Existed"}), status=204)
    token = (Token.objects(user_id=user)).first()
    if not token:
        token = Token(user_id=user)
        token.save()
    session["token"] = token.token_id
    session["user"] = user.to_json()
    print(session['token'])
    return Response(dumps({'status': user.to_json(), 'token': token.token_id}), status=200)

# signup


@accounts.route('signup/', methods=['POST'])
def signup():
    try:
        print(request.json)
        data = request.json
        print(data)
        user = User(**data['user'])
        profile=Profile(**data['profile'],user=user)
        user.save()
       
        return Response(dumps({'message': 'created'}), status=200)
    except Exception as e:
        print(e, 'error')
        return Response(dumps({'message': str(e)}), status=400)


# user id
@accounts.route('user/<id>', methods=['GET', 'PATCH', 'DELETE'])
def user(id):
    user_pipeline = pipeline
    user_pipeline = user_pipeline.insert(0, {'$match': {'_id': int(id)}})
    user = User.objects(id=int(id))
    if not user:
        return Response(dumps({'message': "User doesn't Existed"}), status=400)
    if request.method == 'GET':
        user = User.objects.aggregate(pipeline=user_pipeline)
        return Response(dumps({'status': 'success', 'data': dumps(user)}), status=200)
    elif request.method == 'PATCH':
        data = request.json
        print(data)
        user.update(**data['user'])
        profile = Profile.objects(user=int(id))
        profile.update(**data['profile'])
        return Response(dumps({'status': 'updated successfully', 'data': user.to_json()}), status=200)

    elif request.method == 'DELETE':
        user.delete()
        return Response(dumps({'status': 'deleted successfully'}), status=200)


# logout
@accounts.route('logout/')
def logout():
    session['token'] = None
    session['user'] = None
    return {'status': 'logged out'}

# profile details view


@accounts.route('profile/', methods=['GET'])
@token_required
def profile():
    user = loads(session['user'])
    user_pipeline = pipeline
    user_pipeline.insert(0, {'$match': {'_id': int(user['_id'])}})
    user = User.objects.aggregate(pipeline=user_pipeline)
    return Response(dumps({'status': 'success', 'data': dumps(user)}), status=200)


@accounts.route('check-user/', methods=['GET'])
def check_for_user():
    email = request.args.get('email')
    phone = request.args.get('phone')
    users = User.objects
    for user in users:
        if user.email == email:
            return Response(dumps({'status': 'failure', 'data': 'email altready exists'}), status=204)
        if user.phone == phone:
            return Response(dumps({'status': 'failure', 'data': 'phone altready exists'}), status=204)
    print(email, 'ji', phone)
    return Response(status=200)



# @accounts.route('student')
