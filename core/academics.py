from flask import Blueprint, request, Response, jsonify
from json import dumps, loads
from .models import *
from .utils import token_required
from .models import Chapter

academics = Blueprint('academics', __name__)

# grade


@academics.route('grade/', methods=['POST'])
def grade():
    data = request.json
    try:
        grade = Grade(grade=data['grade'], section=data['section'])
        if grade.validate():
            grade.save()
            return Response(dumps({'message': f" Grade {data['grade']} Created"}), status=200)
        return 'Not a valid grade'
    except Exception as e:
        return Response(dumps({'message': e}), status=400)


@academics.route('grade/<int:id>', methods=['PATCH', 'DELETE'])
def gradeUD(id):
    query = Grade.objects(id=id).get()
    if request.method == 'PATCH':
        print(query.to_json())
        if query:
            data = request.json
            try:
                query.update(grade=data['grade'], section=data['section'])
                return Response(dumps({"message": f"Grade {query.grade} Updated "}), status=200)
            except Exception as e:
                return Response(dumps({'message': str(e)}), status=400)
    if request.method == 'DELETE':
        if query:
            try:
                query.delete()
            except Exception as e:
                return Response(dumps({'message': str(e)}), status=400)


@academics.route('subject/', methods=['POST'])
def subject(id=None):
    print('POST')
    data = request.json
    query = Subject(name=str(data['name']).upper(),
                    code=data['code'], grade=data['grade'])
    try:
        query.save()
        return Response(dumps({'message': f"{data['name']} Created"}), status=200)
    except Exception as e:
        return Response(dumps({'message': str(e)}), status=404)


@academics.route('subject/<int:id>', methods=['PATCH', 'DELETE'])
def subjectUD(id=None):
    if request.method == 'PATCH':
        data = request.json
        query = Subject.objects(id=int(id)).first()
        print(query.to_json())
        if query:
            try:
                code = Subject.objects(code=str(data['code'])).first()
                print(id)
                if code is None or code.id == id:
                    query.update(name=data['name'], code=data['code'])
                    return Response(dumps({'message': f" From Standard {str(query.grade.grade)},Subject {query.name} updated to {data['name']} "}), status=400)
                else:
                    return Response(dumps({'message': f' {code.name} Subject code already exists'}), status=404)
            except Exception as e:
                print(e)
                return Response(dumps({'message': str(e)}), status=400)
    if request.method == 'DELETE':
        subject = Subject.objects(id=id).first()
        subject.delete()
        return Response(dumps({'status': 'success', "data": f"chapter {subject.name} deleted successfully"}))


@academics.route('chapter/', methods=['GET', 'POST'])
# @token_required
def chapter():
    if request.method == "POST":
        data = request.json
        print(data)
        try:
            subject = Subject.objects(id=data['subject_id']).first()
            if not subject:
                return Response(dumps({'status': 'failure', 'data': "subject doesn't exists"}))
            chapter = Chapter(name=data['name'], chapter_no=data['chapter_no'],
                              description=data['description'], subject_id=subject)
            chapter.save()
        except Exception as e:
            return Response(dumps({'message': str(e)}))
        return Response(dumps({'message': f"{data['name']} Created"}))
    if request.method == "GET":
        chapters = Chapter.objects
        print(chapters)
        return Response(dumps({'status': 'success', 'data': chapters.to_json()}), status=200)


@ academics.route('chapter/<id>/', methods=['PATCH', "DELETE"])
def chapter_edit(id):
    chapter = Chapter.objects(id=id).first()
    if not chapter:
        return Response(dumps({'status': 'failure', 'data': "chapter doesn't exists"}))
    if request.method == "PATCH":
        data = request.json
        print(data)
        try:
            for key in data:
                print(key)
                setattr(chapter, key, data[key])
            chapter.save()
            print(chapter)
        except Exception as e:
            print(str(e))
            return Response(dumps({'status': 'failure', 'data': str(e)}))
        return Response(dumps({'status': 'success', 'data': chapter.to_json()}))
    if request.method == "DELETE":
        chapter.delete()
        return Response(dumps({'status': 'success', 'data': 'chapter {} deleted successfully'.format(chapter.name)}))


@ academics.route('chapter-list', methods=['POST'])
def chapter_list():
    data = request.json
    grade = Grade.objects(grade=data['grade']).get()
    if not grade:
        return Response(dumps({'status': 'failure', 'data': "grade doesn't exists"}))
    subject = Subject.objects(grade=str(grade.id),
                              name=data['subject']).first()
    if not subject:
        return Response(dumps({'status': 'failure', 'data': "subject doesn't exists"}))
    chapters = Chapter.objects(subject_id=subject)
    if not len(chapters):
        return Response(dumps({'status': 'failure', 'data': "subject doesn't have chapters"}))
    chapters = loads(chapters.to_json())
    for chapter in chapters:
        chapter['grade'] = grade.grade
        chapter['subject'] = subject.name
        chapter['subject_id'] = subject.id
    return Response(dumps({'status': 'success', 'data': chapters}))


@academics.route('question/', methods=['POST'])
def question():
    data = request.json
    # query = Question(grade=data['grade'],subject=data['subject'],chapter=data['subject'],
    # question=data['question'],duration=data['duration'],mark = data['mark'],chapter_no=data['chapter_no'],question_type=data['question_type'],congitive_level=data['congitive_level'],difficulty_level=data['difficulty_level'])
    question = Question(**data['question'])
    answer = Answer(**data['answer'], question=question)
    try:
        question.save()
        answer.save()
        return Response(dumps({'staus': 'created'}))
    except Exception as e:
        return Response(dumps({'staus': 'question is not created', 'data': str(e)}))
