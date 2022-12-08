import uuid
from mongoengine import Document, StringField, EmailField, IntField, ObjectIdField, ValidationError, ReferenceField, CASCADE, BooleanField, DateField,ListField,SequenceField,DateTimeField
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
    def get_id(self):
        return self.id

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
    created_at = DateField(default=datetime.datetime.now())
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
class Chpaters(Document):
    subject = ReferenceField(Subject,reverse_delete_rule=CASCADE)
    description = StringField(max_length=40)
    chapter_no = IntField()  
    meta = {'collection':'chpaters'}   
    
    def save(self,*args,**kwargs):
        chpaters = Chpaters.objects()
        if chpaters:
        else:
            self.id = 0
        super.save(*args,**kwargs)            
                   
class Question(Document):
   grade = ReferenceField(Grade, reverse_delete_rule=CASCADE)
   subject = ReferenceField(Subject, reverse_delete_rule=CASCADE)
   chapter = ReferenceField(Chpaters,reverse_delete_rule=CASCADE)
   question = StringField(max_length=100)
   duration = IntField()
   mark = IntField()
   chapter_no = IntField()
   created_at = DateField(default=datetime.datetime.now())
   question_type = StringField(max_length=20,choies={ 
        'choices'='questiontype_choice',
        'default=questiontype_choice[0][0]'} )
   congitive_level =  StringField(max_length=20,choies={
    'choieces'='congitive_level',
    'default'='congitive_choice[0][0]'
   }) 
   difficulty_level = StringField(max_length=20,choies=)  
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

    