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
    FileField,
    EmbeddedDocumentField,
    EmbeddedDocument,
    DictField,
    CASCADE,
)
import re
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
    user = ReferenceField(User, reverse_delete_rule=CASCADE)
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
    grade_id = ReferenceField(Grade, reverse_delete_rule=CASCADE, dbref=True)
    created_at = DateField(default=datetime.datetime.now())
    meta = {'collection': 'subject'}

    def validate(self, clean=True):
        print('validate')
        objects = Subject.objects
        sname = str(self.name).upper()
        if objects:
            code = Subject.objects(
                code=(str(self.name[:3]).upper()+str(self.code)).upper())
            subject = Subject.objects(
                grade_id=self.grade_id, name=sname).first()
            print(self.code, 'new')
            if subject:
                print(subject.to_json())
                raise ValidationError(
                    message='Subject already exists for this grade')
            if code:
                raise ValidationError(
                    message='Code already exists give another one')
        else:
            return True

    def update(self, **kwargs):
        code = re.findall('\d+', kwargs['code'])
        name = str(kwargs['name']).upper()
        subcode = name[:3]+code[0]
        subjectcode = Subject.objects(code=subcode, id__ne=self.id).first()
        if subjectcode:
            raise ValidationError({'message': 'Subjectcode already exists'})
        kwargs['name'] = name
        kwargs['code'] = subcode
        return super().update(**kwargs)

    def save(self, *args, **kwargs):
        subjects = Subject.objects
        if subjects:
            self.name = str(self.name).upper()
            self.code = (self.name[:3]+str(self.code)).upper()
        else:
            self.name = str(self.name).upper()
            self.code = (self.name[:3]+str(self.code)).upper()
        super().save(*args, **kwargs)


class Chapter(Document):
    id = SequenceField(primary_key=True)
    name = StringField(max_length=30)
    chapter_no = IntField(min_value=0)
    subject = ReferenceField(
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
    id = SequenceField(primary_key=True)
    grade = ReferenceField(Grade, reverse_delete_rule=CASCADE, dbref=True)
    subject = ReferenceField(Subject, reverse_delete_rule=CASCADE, dbref=True)
    chapter = ReferenceField(Chapter, reverse_delete_rule=CASCADE, dbref=True)
    question = StringField(max_length=150)
    duration = IntField()
    mark = IntField()
    chapter_no = IntField()
    created_at = DateField(default=datetime.datetime.now())
    question_type = StringField(max_length=20, choices={
                                'fill_in_the_blanks', 'MCQ'}, default=None)
    congitive_level = StringField(max_length=20, choices={
                                  'application', 'knowledge', 'comprehension'}, default=None)
    difficulty_level = StringField(
        max_length=20, choies={'medium', 'hard', 'easy'}, default=None)
    answer = IntField(min_value=0)
    # answer=
    meta = {'collection': 'questions'}

    def validate(self, clean=True):
        self.chapter_no = self.chapter.chapter_no
        return super().validate(clean)


class Answer(Document):
    id = SequenceField(primary_key=True)
    question = ReferenceField(
        Question, reverse_delete_rule=CASCADE, dbref=True)
    option_a = StringField(max_length=40)
    option_b = StringField(max_length=40)
    option_c = StringField(max_length=40)
    option_d = StringField(max_length=40)
    correctanswer = StringField(
        choices={"option_d", "option_c", "option_b", "option_a"})


class Question_paper(Document):
    id = SequenceField(primary_key=True)
    grade = ReferenceField(Grade, reverse_delete_rule=CASCADE)
    subject = ReferenceField(Subject, reverse_delete_rule=CASCADE)
    file = FileField(upload_to='question_files/')
    created_by = StringField(max_length=20)
    created_at = DateTimeField(default=datetime.datetime.now())
    test_uid = StringField(max_length=25)
    question_list = ListField()
    timing = IntField(min_value=0)
    overall_marks = IntField(min_value=0)

    def __str__(self):
        return (str(self.grade)+' '+str(self.subject))


class Test(Document):
    id = SequenceField(primary_key=True)
    question_paper = ReferenceField(
        Question_paper, reverse_delete_rule=CASCADE, dbref=True)
    grade = ReferenceField(Grade, reverse_delete_rule=CASCADE, dbref=True,)
    subject = ReferenceField(Subject, reverse_delete_rule=CASCADE, dbref=True)
    duration = IntField()
    created_staff_id = ReferenceField(
        User, reverse_delete_rule=CASCADE, dbref=True)
    mark = IntField()
    remarks = StringField(max_length=250)
    description = StringField(max_length=100)
    test_uid = StringField()
    pass_percentage = IntField()
    meta = {'collection': 'test'}

    def validate(self, clean=False):
        if not self.test_uid:
            self.test_uid = (str(uuid.uuid4()))[:16]
        if not self.duration:
            self.duration = self.question_paper.timing
        if not self.mark:
            self.mark = self.question_paper.overall_marks
        return super().validate(clean)


class Testresult(Document):
    id = SequenceField(primary_key=True)
    student_id = ReferenceField(User, reverse_delete_rule=CASCADE, dbref=True)
    grade = ReferenceField(Grade, reverse_delete_rule=CASCADE, dbref=True)
    subject = ReferenceField(Subject, reverse_delete_rule=CASCADE, dbref=True)
    test_id = ReferenceField(Test, reverse_delete_rule=CASCADE, dbref=True)
    question_paper = ReferenceField(
        Question_paper, reverse_delete_rule=CASCADE, dbref=True)
    result = StringField(max_length=20)
    score = IntField()
    correct_answer = IntField()
    wrong_answer = IntField()
    unanswer_question = IntField()
    test_details = ListField(DictField())
    created_at = DateTimeField(default=datetime.datetime.now())
    meta = {'collection': 'testresult'}


class Question_bank(Document):
    id = SequenceField(primary_key=True)
    grade = ReferenceField(Grade, reverse_delete_rule=CASCADE)
    subject = ReferenceField(Subject, reverse_delete_rule=CASCADE)
    meta = {'collection': 'question_bank'}


class Instruction(Document):
    id = SequenceField(primary_key=True)
    note = StringField(max_length=250)
    meta = {'collection': 'instruction'}

    def validate(self, clean=False):
        objects = Instruction.objects(note=self.note).first()
        if objects and objects.note == self.note:
            return False
        else:
            return True
