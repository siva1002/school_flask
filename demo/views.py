
from .models import User
from flask import Blueprint,render_template, request, flash, jsonify
views=Blueprint('views',__name__)
from . import db
@views.route('/')
def index():
    return 'Hello, world'

@views.route('/signup',methods = ['POST','GET'])
def signup():
    if request.method == 'POST':
        email=request.form['email']
        firstname=request.form['fname']
        lastname=request.form['lname']
        fullname=request.form['flname']
        address=request.form['ad']
        user=User(email=email,firstname=firstname,lastname=lastname,fullname=fullname,address=address)
        db.session.add(user)
        db.session.commit()
    return render_template('signup.html')
    