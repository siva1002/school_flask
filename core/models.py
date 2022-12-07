
import datetime
import uuid
from mongoengine import Document, StringField, EmailField, IntField, ObjectIdField, ValidationError, ReferenceField, CASCADE, BooleanField, DateField,ListField
from flask_login import UserMixin


class User(Document, UserMixin):
    id = IntField(required=True, primary_key=True)
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

    def clean(self):
        users = User.objects
        if users:
            self.id = (users[users.count()-1]).id + 1
        else:
            self.id = 0
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
        super().save(*args, **kwargs)


class Profile(Document):
    _id = IntField(primary_key=True, required=True)
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
    _id = IntField(primary_key=True, requried=True)
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
    def save(self,*args,**kwargs):
        grades = Grade.objects
        if grades:
            self.id = grades.count()
        else:
            self.id = 1
        super().save(*args, **kwargs)
   



class Subject(Document):
    _id = IntField(primary_key=True, requried=True)
    name = StringField(max_length=20)
    code = IntField()
    grade = ReferenceField(Grade, reverse_delete_rule=CASCADE)
    created_at = DateField(default=datetime)

    def _init_(self, name, code, grade, created_at):
        self.name = name
        self.code = code
        self.created_at = created_at
    meta = {'collection': 'subject'}
    def validate(self,clean=False):
        objects=Subject.objects(name=self.name).first()
        print(self.to_json())
        if objects:
            return False
        else:
            return True

    def save(self,*args,**kwargs):
        subjects = Subject.objects
        if subjects:
            self.id = subjects.count()
            self.code=self.name[:3]+str(self.code)
        else:
            self.id = 1
            self.code=self.name[:4]+str(self.code)
        super(Subject,self).save(*args, **kwargs)
