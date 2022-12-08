import uuid
from mongoengine import Document, StringField, EmailField, IntField, ObjectIdField, ValidationError, ReferenceField, CASCADE, BooleanField, DateField,ListField,SequenceField
from flask_login import UserMixin
import datetime

class User(Document, UserMixin):
    id = SequenceField(primary_key=True)
    email = EmailField(required=True)
    phone = IntField(required=True)
    registernumber = StringField(required=True)
    usertype = StringField(
        choices={'is-Admin', 'is-Staff', 'is-Student'}, default=None)
    is_active = BooleanField(default=True)
    meta = {'collections': 'user'}

    def _init__(self, email, phone, registernumber):
        self.email = email
        self.phone = phone
        self.registernumber = registernumber

    def get_id(self):
        return self.id

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

    def _init__(self, firstname, fullname, lastname, address, user):
        self.fullname = fullname
        self.lastname = lastname
        self.address = address
        self.firstname = firstname
    meta = {'collection': 'profile'}

    def clean(self):
        users = Profile.objects
        # if users(email__exists=self.email):
        #     raise ValidationError({'error': 'altready exists'})
        if users:
            self.id = users.count()
        else:
            self.id = 1
        print(users)


class Grade(Document):
    id = SequenceField(primary_key=True)
    grade = IntField()
    section = ListField()

    def _init_(self, grade, section):
        self.grade = grade
        self.section = section
    meta = {'collection': 'grade'}
    def validate(self,clean=False):
        objects=Grade.objects(grade=self.grade).first()
        if objects and objects.grade == self.grade:
            return False
        else:
            return True
   
class Subject(Document):
    id = SequenceField(primary_key=True)
    name = StringField(max_length=20)
    code = StringField(max_length=20)
    grade = ReferenceField(Grade, reverse_delete_rule=CASCADE,dbref = True)
    created_at = DateField(default=datetime)

    def _init_(self, name, code, created_at):
        self.name = name
        self.code = code
        self.created_at = created_at
    meta = {'collection': 'subject'}
    def validate(self,clean=False):
            objects=Subject.objects()
            print(objects)
            print(self.to_json())
            if objects:
                objects=Subject.objects(name=self.name,grade=self.grade).first()
                code=Subject.objects(code=(self.name[:3]+str(self.code)).upper()).first()
                if objects or code:
                    return False
                return True
            else:
                return True
    def save(self,*args,**kwargs):
        subjects = Subject.objects
        if subjects:
            self.code=(self.name[:3]+str(self.code)).upper()
        else:
            self.code=self.name[:3]+str(self.code)
        super().save(*args, **kwargs)
