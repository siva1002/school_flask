from . import db
class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    fullname = db.Column(db.String(128))
    firstname = db.Column(db.String(128))
    lastname = db.Column(db.String(128))
    email= db.Column(db.String(30),unique=True)
    address = db.Column(db.String(100))
    def __init__(self,email,fullname,lastname,firstname,address):
        self.fullname=fullname
        self.firstname=firstname
        self.lastname=lastname
        self.email=email
        self.address=address
        