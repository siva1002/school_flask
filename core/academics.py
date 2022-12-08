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

@academics.route('subject/<id>',methods=['PATCH','DELETE'])
@academics.route('subject/', methods=['POST'])
def subject(id=None):
    if request.method=='POST':
        data = request.json
        # try:
        query = Subject(name=str(data['name']).upper(),code=data['code'],grade=data['grade'])
        try:
            query.save()
            return Response(dumps({'message': f"{data['name']} Created"}), status=200)
        except Exception as e:
            return Response(dumps({'message': str(e)}), status=404)

    if request.method=='PATCH':
        data=request.json
        query = Subject.objects(id=int(id)).first()
        print(query.to_json())
        if query:
            try:
                code=Subject.objects(code=str(data['code'])).first()
                if code is None:
                    query.update(name=data['name'], code=data['code'])
                    return Response(dumps({'message': f"Subject {query.name} updated"}), status=400)
                else:
                    return Response(dumps({'message':f' {code.name} Subject code already exists'}), status=404)
            except Exception as e:
                print(e)
                return Response(dumps({'message':str(e)}), status=400)
    if request.method =='DELETE':
        subject = Subject.objects(id=id).first()
        subject.delete()
        return Response(dumps({'status': 'success', 'data': 'chapter {} deleted successfully'.format(subject.name)}))

@academics.route('chapter/', methods=['GET', 'POST'])
# @token_required
def chapter():
    if request.method == "POST":
        data = request.json
        print(data)
        try:
            subject = Subject.objects(id=data['subject_id']).first()
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


@academics.route('chapter/<id>/', methods=['PATCH', "DELETE"])
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
