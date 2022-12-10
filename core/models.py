from mongoengine import (
    Document,
    SequenceField,
    StringField,
    EmailField,
    IntField,
    ValidationError,
    ReferenceField,
    BooleanField,
    DateField,
    ListField,
    DateTimeField,
    EmbeddedDocumentField,
    EmbeddedDocument,
    DictField,
    CASCADE,
)
import datetime
from flask_login import UserMixin
import uuid
class User(Document, UserMixin):
    id = SequenceField(primary_key=True)
    email = EmailField(required=True)
    phone = IntField(required=True)
    registernumber = StringField(required=True)
    usertype = StringField(
        choices={'is-admin', 'is-staff', 'is-student'}, default=None)
    is_active = BooleanField(default=True)
    meta = {'collections': 'user'}

    def get_id(self):
        return self.id

    def validate(self, clean=True):
        user = User.objects
        if user(email=self.email):
            raise ValidationError(message='email already exists')
        if user(phone=self.phone):
            raise ValidationError(message='phone altready exists')
        if user(registernumber=self.registernumber):
            raise ValidationError(message='register number altready exists')
        return super().validate(clean)



class Profile(Document):
    id = SequenceField(primary_key=True)
    firstname = StringField(max_length=50)
    lastname = StringField(max_length=50)
    fullname = StringField(max_length=50)
    address = StringField(max_length=100)
    standard = ListField()
    user=ReferenceField(User,reverse_delete_rule=CASCADE)
    meta = {'collection': 'profile'}

class Token(Document):
    user_id = ReferenceField(document_type=User, reverse_delete_rule=CASCADE)
    token_id = StringField()
    meta = {'collections': 'token'}

    def save(self, *args, **kwargs):
        self.token_id = str(uuid.uuid4())
        super().save(*args, **kwargs)


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
            code = Subject.objects(
                code=(str(self.name[:3]).upper()+str(self.code)).upper())
            subject = Subject.objects(grade=self.grade, name=self.name)
            print(self.code, 'new')
            if subject:
                print(subject.to_json())
                raise ValidationError(
                    message='Subject already exists for this grade')
            if code:
                print(code.to_json())
                raise ValidationError(
                    message='Code already exists give another one')

        else:
            return True

    def save(self, *args, **kwargs):
        subjects = Subject.objects
        if subjects:
            self.code = (self.name[:3]+str(self.code)).upper()
            self.name = str(self.name).upper()
        else:
            self.name = str(self.name).upper()
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
        subject = Subject.objects(id=self.subject_id.id).first()
        chapters = Chapter.objects(subject_id=subject)
        if self.id:
            chapters = chapters(id__ne=self.id)
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
   question = StringField(max_length=150)
   duration = IntField()
   mark = IntField()
   chapter_no = IntField()
   created_at = DateField(default=datetime.datetime.now())
   question_type = StringField(max_length=20,choices={'filling_in_blanks','MCQ'},default= None)
   congitive_level =  StringField(max_length=20,choices={ 'application','knowledge','comprehension'},default=None)
   difficulty_level = StringField(max_length=20,choies={'medium','hard','easy'},default=None)
   meta = {'collection':'questions'}  
class Answer(Document):
    id = SequenceField(primary_key=True)
    question=ReferenceField(Question,reverse_delete_rule=CASCADE,dbref=True)
    option_a=StringField(max_length=40)
    option_b=StringField(max_length=40)
    option_c=StringField(max_length=40)
    option_d=StringField(max_length=40)
    correctanswer = StringField(choices={"option_d","option_c","option_b","option_a"})
   
class Instruction(Document):
    note = StringField(max_length=250)
    meta = {'collection':'instruction'}

class Test(Document):
    # question_paper= ReferenceField(Question_paper,reverse_delete_rule=CASCADE)
    grade = ReferenceField(Grade,reverse_delete_rule=CASCADE)
    subject = ReferenceField(Subject,reverse_delete_rule=CASCADE)
    duration = IntField()
    mark = IntField()
    remarks = StringField(max_length=250)
    description = StringField(max_length=100)
    test_id = IntField()
    pass_percentage = IntField()
    meta = {'collection':'test'}
class Testresult(Document):
    student_id = ReferenceField(User,reverse_delete_rule=CASCADE)
    grade = ReferenceField(Grade,reverse_delete_rule=CASCADE)
    subject = ReferenceField(Subject,reverse_delete_rule=CASCADE)
    test_id = ReferenceField(Test,reverse_delete_rule=CASCADE)
    # question_paper = ReferenceField(Question_paper,reverse_delete_rule=CASCADE)
    result = StringField(max_length=20)
    score = IntField()
    correct_answer = IntField()
    worong_answer = IntField()
    unanswer_question = IntField()
    meta ={'collection':'testresult'}
class QuestionBank(Document):
    grade = ReferenceField(Grade,reverse_delete_rule=CASCADE)
    subject = ReferenceField(Subject,reverse_delete_rule=CASCADE)
    meta = {'collection':'question_bank'}

