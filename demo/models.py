from .extension import db
from flask_migrate import Migrate
from flask_serialize import FlaskSerialize
from sqlalchemy.dialects.postgresql import ARRAY
fxmixn=FlaskSerialize(db)
class User(fxmixn,db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    email= db.Column(db.String(30),unique=True)
    register_number = db.Column(db.String(15),unique=True)
    phone= db.Column(db.String(10),unique=True)
    address = db.Column(db.String(100))
    __fs_create_fields__ = __fs_update_fields__ = ['email','address','phone','register_number']
    def __init__(self,email,register_number,phone,address):
        self.phone=phone
        self.register_number=register_number
        self.email=email
        self.address=address
    def __repr__(self):
        return self.fullname
class Profile(fxmixn,db.Model):
    __tablename__ = 'profile'
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.Integer, db.ForeignKey('user.id'))
    user_type=db.Column(db.String(30))
    fullname = db.Column(db.String(128))
    firstname = db.Column(db.String(128))
    lastname = db.Column(db.String(128))
    standard = db.Column(db.String(128))
    section= db.Column(ARRAY(db.String))
    __fs_create_fields__ = __fs_update_fields__ = ['fullname', 'firstname', 'lastname', 'standard', 'section','address']
    def __init__(self,standard,fullname,lastname,firstname,address,user,user_type):
        self.standard = standard
        self.fullname = fullname
        self.lastname = lastname
        self.firstname = firstname
        self.address = address
        self.user_type=user_type