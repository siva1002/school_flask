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


@academics.route('subject/', methods=['POST'])
def subject():
    data = request.json
    try:
        query = Subject(name=data['name'],
                        code=data['code'], grade=data['grade_id'])
        if query.validate():
            query.save()
            return Response(dumps({'message': f"{data['name']} Created"}), status=200)
        return Response(dumps({'message': "Not Created"}), status=404)
    except Exception as e:
        return Response(dumps({'message': e}), status=400)


@academics.route('chapter/', methods=['POST'])
# @token_required
def chapter():
    data = request.json
    chapter = Chapter(name=data['name'], chapter_no=data['chapter_no'],
                      description=data['description'], subject_id=data['subject_id'])
    chapter.save()
    return chapter.to_json()
