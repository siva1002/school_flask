from flask import Blueprint, request, Response, jsonify
from json import dumps, loads
from .models import *


academics = Blueprint('academics', __name__)

# grade


@academics.route('grade/', methods=['GET', 'POST'])
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
