from .extension import db
from flask_serialize import FlaskSerialize
from sqlalchemy.dialects.postgresql import ARRAY
fxmixn = FlaskSerialize(db)

class User(fxmixn, db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(30), unique=True)
    register_number = db.Column(db.String(15), unique=True)
    phone = db.Column(db.String(10), unique=True)
    address = db.Column(db.String(110))
    profile = db.relationship('Profile', backref='user', uselist=False)
    token = db.relationship('Token', backref='user', uselist=False)
    __fs_create_fields__ = __fs_update_fields__ = [
        'email', 'address', 'phone', 'register_number']

    def __init__(self, email, register_number, phone, address):
        self.phone = phone
        self.register_number = register_number
        self.email = email
        self.address = address

    def save(self):
        db.session.add(self)
        db.session.commit()
        return self.id

    def __repr__(self):
        return self.email


class Profile(fxmixn, db.Model):
    __tablename__ = 'profile'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user_type = db.Column(db.String(30))
    fullname = db.Column(db.String(128))
    firstname = db.Column(db.String(128))
    lastname = db.Column(db.String(128))
    standard = db.Column(db.String(128))
    section = db.Column(ARRAY(db.String))
    __fs_create_fields__ = __fs_update_fields__ = [
        'fullname', 'firstname', 'lastname', 'standard', 'section', 'address']
    __fs_relationship_fields__ = ['user_id']

    def __init__(self, standard, fullname, lastname, firstname, user_type, user_id):
        self.standard = standard
        self.fullname = fullname
        self.lastname = lastname
        self.firstname = firstname
        self.user_type = user_type
        self.user_id = user_id

    def save(self):
        db.session.add(self)
        db.session.commit()


class Token(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
  token=db.Column(db.String(200))
  def __init__(self,user_id,token):
    self.user_id = user_id
    self.token=token
  def save(self):
    db.session.add(self)
    db.session.commit()
