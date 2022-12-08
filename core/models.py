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
    meta = {'collection': 'profile'}


class Grade(Document):
    id = SequenceField(primary_key=True)
    grade = IntField()
    section = ListField()
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
    created_at = DateField(default=datetime.datetime.now())
    meta = {'collection': 'subject'}

    def validate(self, clean=True):
        objects = Subject.objects
        if objects:
            objects = Subject.objects(name=self.name , grade=self.grade).first()
            print(objects)
            code = Subject.objects(
                code=(self.name[:3]+str(self.code)).upper()).first()
            if objects:
                raise ValidationError(
                    message='Subject already exists for this grade')
            if code:
                raise ValidationError(
                    message='Code already exists give another one')
        else:
            return True

    def save(self, *args, **kwargs):
        subjects = Subject.objects
        if subjects:
            self.code = (self.name[:3]+str(self.code)).upper()
            self.name=str(self.name).upper()
        else:
            self.code = (self.name[:3]+str(self.code)).upper()
        super().save(*args, **kwargs)


class Chapter(Document):
    id = SequenceField(primary_key=True)
    name = StringField(max_length=30)
    chapter_no = IntField(min_value=0)
    subject_id = ReferenceField(
        Subject, reverse_delete_rule=CASCADE, dbref=True)
    description = StringField(max_length=50)
    created_at = DateTimeField(default=datetime.datetime.now())
    meta = {'collection': 'chapters'}

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
        return super().validate(clean)
class Question(Document):
   grade = ReferenceField(Grade, reverse_delete_rule=CASCADE)
   subject = ReferenceField(Subject, reverse_delete_rule=CASCADE)
   chapter = ReferenceField(Chapter,reverse_delete_rule=CASCADE)
   question = StringField(max_length=100)
   duration = IntField()
   mark = IntField()
   chapter_no = IntField()
   created_at = DateField(default=datetime.datetime.now())
   question_type = StringField(max_length=20,choies={ 
        'choices'='questiontype_choice',
        'default=questiontype_choice[0][0]'} )
   congitive_level =  StringField(max_length=20,choies={
    'choices'='congitive_level',
    'default'='congitive_choice[0][0]'
   }) 
   difficulty_level = StringField(max_length=20,choies={
    'choices'='difficulty_level',
    'default'='difficulty_choice[0][0]'
   })  
   meta = {'collection':'questions'}  
   def clean(self):
       question = Question.objects()
       if question:
         self.id = question.count()  
       else:
        self.id = 0
   def save(self,*args,**kwargs):
        question = Question.objects()
        if question:
            self.id= question.count()
        else:
            self.id = 0
        super.save(*args,**kwargs)    
