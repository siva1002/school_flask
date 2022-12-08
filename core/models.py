import uuid
from flask_login import UserMixin
from pydantic import BaseModel, Field
from typing import Optional
from bson import ObjectId
import json
import datetime
import uuid
from mongoengine import Document, SequenceField, StringField, EmailField, IntField, ObjectIdField, ValidationError, ReferenceField, CASCADE, BooleanField, DateField, ListField, DateTimeField
from flask_login import UserMixin
import datetime


class User(Document, UserMixin):
    id = SequenceField(primary_key=True)
    email = EmailField(required=True)
    phone = IntField(required=True)
    user_type = StringField(
        choices={'is_admin', 'is_staff', 'is_student'}, default=None)
    registernumber = StringField(required=True)
    usertype = StringField(
        choices={'is-Admin', 'is-Staff', 'is-Student'}, default=None)
    is_active = BooleanField(default=True)
    meta = {'collections': 'user'}

    def _init__(self, email, phone, registernumber, user_type):
        self.email = email
        self.phone = phone
        self.registernumber = registernumber
        self.user_type = user_type

    def get_id(self):
        return self.id


    def validate(self, clean=True):
        user = User.objects
        if user(email=self.email):
            raise ValidationError(message='email altready exists')
        if user(phone=self.phone):
            raise ValidationError(message='phone altready exists')
        if user(registernumber=self.registernumber):
            raise ValidationError(message='register number altready exists')
        return super().validate(clean)


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
    id = SequenceField(primary_key=True)
    firstname = StringField(max_length=50)
    lastname = StringField(max_length=50)
    fullname = StringField(max_length=50)
    address = StringField(max_length=100)
    user = ReferenceField(User, reverse_delete_rule=CASCADE)

    def _init__(self, firstname, fullname, lastname, address):
        self.fullname = fullname
        self.lastname = lastname
        self.address = address
        self.firstname = firstname
    meta = {'collection': 'profile'}

class Grade(Document):
    id = SequenceField(primary_key=True)
    grade = IntField()
    section = ListField()

    def _init_(self, grade, section):
        self.grade = grade
        self.section = section
    meta = {'collection': 'grade'}

    def validate(self, clean=False):
        objects = Grade.objects(grade=self.grade).first()
        if objects and objects.grade == self.grade:
            return False
        else:
            return True


class Subject(Document):
    id = SequenceField(primary_key=True)
    name = StringField(max_length=20)
    code = StringField(max_length=20)
    grade = ReferenceField(Grade, reverse_delete_rule=CASCADE, dbref=True)
    created_at = DateField(default=datetime)

    def _init_(self, name, code, created_at):
        self.name = name
        self.code = code
        self.created_at = created_at
    meta = {'collection': 'subject'}

    def validate(self, clean=False):
        objects = Subject.objects()
        if objects:
            objects = Subject.objects(name=self.name, grade=self.grade).first()
            code = Subject.objects(
                code=(self.name[:3]+str(self.code)).upper()).first()
            if objects:
                raise ValidationError(message='Subject already exists for this grade')
            if code:
                raise ValidationError(message='Code already exists give another one')
        else:
            return True

    def save(self, *args, **kwargs):
        subjects = Subject.objects
        if subjects:
            self.code = (self.name[:3]+str(self.code)).upper()
        else:
            self.code = self.name[:3]+str(self.code)
        super().save(*args, **kwargs)


class Chapter(Document):
    id = SequenceField(primary_key=True)
    name = StringField(max_length=30)
    chapter_no = IntField(min_value=0)
    subject_id = ReferenceField(Subject, reverse_delete_rule=CASCADE)
    description = StringField(max_length=50)
    created_at = DateTimeField(default=datetime.datetime.now())
    meta = {'collection': 'chapters'}

    def _init_(self, name, chapter_no, subject_id, description):
        self.name = name
        self.chapter_no = chapter_no
        self.description = description
        self.subject_id = subject_id

    def validate(self, clean=True):
        subject = Subject.objects(id=self.subject_id).first()
        chapters = Chapter.objects(subject_id=subject)
        if not subject:
            raise ValidationError(message="subject dosn't exists")
        if chapters(chapter_no=self.chapter_no):
            raise ValidationError(message="chapter no in this altready exists")
        if chapters(name=self.name):
            raise ValidationError(
                message="this subject has the chapter in this name altready")
        self.subject_id = subject
        return super().validate(clean)
