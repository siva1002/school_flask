from pydantic import BaseModel, Field
from typing import Optional
from bson import ObjectId
import json
import datetime
import uuid
from mongoengine import Document, StringField, EmailField, IntField, ObjectIdField, ValidationError, ReferenceField, CASCADE, BooleanField
from flask_login import UserMixin
class User(Document, UserMixin):
    id = IntField(required=True, primary_key=True)
    email = EmailField(required=True)
    phone = IntField(required=True)
    registernumber=StringField(required=True)
    is_active = BooleanField(default=True)
    meta = {'collections': 'user'}

    def _init__(self, email, phone,registernumber):
        self.email = email
        self.phone = phone
        self.registernumber=registernumber

    def get_id(self):
        return self.id

    def clean(self):
        users = User.objects
        # if users(email__exists=self.email):
        #     raise ValidationError({'error': 'altready exists'})
        if users:
            self.id = users.count()
        else:
            self.id = 0
        print(users)

    def __repr__(self):
        return self.email
class Token(Document):
    user_id = ReferenceField(document_type=User, reverse_delete_rule=CASCADE)
    token_id = StringField()
    meta = {'collections': 'token'}

    def _init__(self, user_id, token_id):
        self.user_id = user_id
        self.token_id = token_id

    def save(self, *args, **kwargs):
        self.token_id = str(uuid.uuid4())
        super().save(*args, **kwargs)
class Profile(Document):
    _id=IntField(primary_key=True,required=True)
    firstname = StringField(max_length=50)
    lastname = StringField(max_length=50)
    fullname= StringField(max_length=50)
    usertype = StringField(max_length=10)
    address = StringField(max_length=100)
    user=ReferenceField(User,reverse_delete_rule=CASCADE)
    def _init__(self,firstname,fullname,lastname,usertype,address,user):
      self.fullname=fullname
      self.lastname=lastname
      self.usertype=usertype
      self.address=address
      self.firstname = firstname
    meta={'collection': 'profile'}
    def clean(self):
        users = Profile.objects
        # if users(email__exists=self.email):
        #     raise ValidationError({'error': 'altready exists'})
        if users:
            self.id = users.count()
        else:
            self.id = 0
        print(users)
    def __repr__(self):
        return self.fullname
   
