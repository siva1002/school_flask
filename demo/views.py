from .models import User,Profile
from flask import Blueprint,render_template, request, flash, jsonify
views=Blueprint('views',__name__)
from .extension import db
@views.route('/')
def index():
    return 'Hello, world'

@views.route('signup/',methods = ['POST','GET','PUT'])
def signup():
    if request.method == 'POST':
        email=request.form['email']
        firstname=request.form['fname']
        lastname=request.form['lname']
        fullname=request.form['flname']
        address=request.form['ad']
        phone=request.form['phone']
        reg=request.form['reg']
        user=User(email=email,register_number=reg,address=address,phone=phone)
        db.session.add(user)
        db.session.commit()
        print(user.id)
        pro=Profile(standard=request.form['std'],firstname=firstname,lastname=lastname,fullname=fullname,user_type='is_student',user=int(user.id),address=address)
        db.session.add(pro)
        db.session.commit()
    return render_template('signup.html')
@views.route('/api',methods=['GET'])
def api():
      return User.fs_get_delete_put_post(prop_filters = {'phone':'9942945428'})
@views.route('/log')
def log():
    user=User.query.filter_by(address='student').first()
    
    return {'address':user.address}
