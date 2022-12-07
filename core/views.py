from .models import User, Profile, Token
from mongoengine import connect, get_db
from bson.json_util import dumps, loads
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
            token_id = ((request.headers['Authorization']).split(' '))[1]
        token = Token.objects(token_id=token_id).first()
        if not token:
            return {'data': 'invalid token'}
        user = User.objects(id=token.user_id.id).first()
        print(user)
        session['token'] = token_id
        session['user'] = user.to_json()
        user = token.user_id
        return f(*args, **kwargs)
    return decorated_function


@views.route('/')
@token_required
def userdetails():
    user = loads(session['user'])
    print(user['user_type'])
    pipeline = [{"$lookup": {
        "from": "profile",
        "localField": "_id",
        "foreignField": 'user',
        "as": 'profile'
    }}]
    if user['user_type'] == 'is_admin':
        queryset = User.objects.aggregate(pipeline=pipeline)
    elif user['user_type'] == 'is_staff':
        pipeline.insert(
            0, {'$match': {'user_type': 'is_student'}})
        queryset = User.objects.aggregate(
            pipeline=pipeline)
    else:
        pipeline.insert(
            0, {'$match': {'_id': int(user['_id'])}})
        queryset = User.objects.aggregate(
            pipeline=pipeline)
    queryset = dumps(queryset)
    return {'status': 'success', 'data': queryset}


@views.route('login/', methods=['POST'])
def login():
    data = request.get_json()
    user = User.objects(email=data['email'], phone=data['phone'])[0]
    token = (Token.objects(user_id=user)).first()
    if not token:
        token = Token(user_id=user)
        token.save()
    session["token"] = token.token_id
    session["user"] = user.to_json()
    print(session['token'])
    return {'status': user.to_json(), 'token': token.token_id}


@views.route('/')
@token_required
def index():
    return 'Hello, world'


@views.route('signup/', methods=['POST'])
def signup():
    try:
        print(request.json)
        data = request.json

        user = User(email=data['email'], phone=data['phone'],
                    registernumber=data['registernumber'], user_type=data['user_type'])

        user.save()
        profile = Profile(fullname=data['fullname'], firstname=data["firstname"],
                          lastname=data['lastname'], address=data['address'], user=user)
        profile.save()
        return Response(dumps({'message': 'created'}), status=200)
    except Exception as e:
        print(e, 'error')
        return Response(dumps({'message': 'not created'}), status=400)


@views.route('user/<id>', methods=['GET', 'PATCH', 'DELETE'])
def user(id):
    pipeline = [{'$match': {'_id': int(id)}}, {"$lookup": {
        "from": "profile",
        "localField": "_id",
        "foreignField": 'user',
        "as": 'profile'
    }}]
    user = User.objects(id=int(id))
    if not user:
        return Response({'message': "User doesn't Existed"}, status=400)
    if request.method == 'GET':
        user = User.objects.aggregate(pipeline=pipeline)
        return Response(dumps({'status': 'success', 'data': dumps(user)}), status=200)
    elif request.method == 'PATCH':
        data = request.json
        print(data)
        user.update(email=data['email'], phone=data['phone'],
                    registernumber=data['registernumber'], user_type=data['user_type'])
        profile = Profile.objects(user=int(id))
        profile.update(fullname=data['fullname'], firstname=data["firstname"],
                       lastname=data['lastname'], address=data['address'])
        return Response(dumps({'status': 'updated successfully', 'data': user.to_json()}), status=200)

    elif request.method == 'DELETE':
        user.delete()
        return Response(dumps({'status': 'deleted successfully'}), status=200)


@views.route('logout/')
def logout():
    session['token'] = None
    session['user'] = None
    return {'status': 'logged out'}
