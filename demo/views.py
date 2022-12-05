import uuid
from . serializer import UserSerializer
from .extension import db
# from . import app
from .models import User, Profile,Token
from flask import Blueprint, render_template, request,jsonify,make_response
import jwt
from flask_pymongo import PyMongo
views = Blueprint('views', __name__)
@views.route('/')
def index():

    return 'Hello, world'
    
@views.route('signup/', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST': 
        email = request.form['email']
        firstname = request.form['fname']
        lastname = request.form['lname']
        fullname = request.form['flname']
        address = request.form['ad']
        phone = request.form['phone']
        reg = request.form['reg']
        usertype = request.form['usertype']
        # data=request.get_json()
        # email=data['email']
        # firstname=data['fname']
        # lastname=data['lname']
        # fullname=data['flname']
        # address=data['ad']
        # phone=data['phone']
        # reg=data['reg']
        if usertype == 'is_admin' or usertype == 'is_staff':
            if usertype != 'is_admin':
                user = User(email=email, register_number=reg,
                            address=address, phone=phone)
                user = user.save()
                pro = Profile(standard=request.form['std'], firstname=firstname,
                              lastname=lastname, fullname=fullname, user_type='is_staff', user_id=user)
                pro.save()
            user = User(email=email, register_number=reg,
                        address=address, phone=phone)
            user = user.save()
            pro = Profile(standard=request.form['std'], firstname=firstname,
                          lastname=lastname, fullname=fullname, user_type='is_admin', user_id=user)
            pro.save()
        else:
            user = User(email=email, register_number=reg,
                        address=address, phone=phone)
            user = user.save()
            pro = Profile(standard=request.form['std'], firstname=firstname,
                          lastname=lastname, fullname=fullname, user_type='is_student', user_id=user)
            pro.save()
    return render_template('signup.html')
# @token_required
@views.route('/api/', methods=['GET'])
def api():
    headers=request.headers
    print(request.headers)
    user = User.query.get(1)
    print(user)
    print(user.profile.lastname)
    user = User.query.all()
    seraialize = UserSerializer(many=True)
    data = seraialize.dump(user)
    return data


@views.route('/users', methods=['GET', 'PUT'])
def log():
    print(request.user)


@views.route('/login/', methods=['GET', 'POST'])
def login():
    if request.method=='POST':
        data=request.get_json()
        # email=request.form['email']
        # phone=request.form['phone']
        email=data['email']
        phone=data['phone']
        print(email)
        print(phone)
        user=User.query.filter_by(email=email,phone=phone).first()
        print(User.query.filter_by(email=email,phone=phone).count()) 
        if user:
            try:
                if Token.query.get(user.id):
                    return {'token': user.token.token,
                            'user-type': user.profile.user_type
                            }
                else:
                    token=Token(user_id=user.id,token=str(uuid.uuid4()))
                    token.save()
                    return {'token':token.token,
                            'user-type':user.profile.user_type
                    }
            except:
                return make_response('Something went wrong')
        else:
            return make_response('User Does Not Exist')
            
