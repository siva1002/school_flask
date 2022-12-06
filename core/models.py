# from .extension import db
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
    is_active = BooleanField(default=True)
    meta = {'collections': 'user'}

    def _init__(self, email, phone):
        self.email = email
        self.phone = phone

    def get_id(self):
        return self.id

    def clean(self):
        users = User.objects
        # if users(email__exists=self.email):
        #     raise ValidationError({'error': 'altready exists'})
        self.id = users.count()
        print(users)


class Token(Document):
    user_id = ReferenceField(document_type=User, reverse_delete_rule=CASCADE)
    token_id = StringField()
    meta = {'collections': 'token'}

    def _init__(self, user_id, token_id):
        self.user_id = user_id
        self.token_id = token_id

    def save(self, *args, **kwargs):
        self.token_id = str(uuid.uuid4())
        super(Token, self).save(*args, **kwargs)


# class JSONEncoder(json.JSONEncoder):
#     def default(self, o):
#         print(self, o)
#         if isinstance(o, ObjectId):
#             return str(o)
#         if isinstance(o, datetime):
#             return str(o)
#         return json.JSONEncoder.default(self, o)
