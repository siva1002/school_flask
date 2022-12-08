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
@academics.route('subject/',methods=['GET','POST'])  
def sub():
    data = request.json
    try:
        subject = Subject(name=data['name'],grade=grade,
        code=data['code'],created_at=data['created_at']) 
        subject.save()
        return Response(dumps({'message':f"Subject{data['code']}created"}),status=200)
    except Exception as e:
        return Response(dumps({'message':e}),status=404) 
@academics.route('update<pk>/',methods = ['PATCH'])
def updatedsub(id):
    data = request.json
    try:
        subjets = Subject.update.one({'id':ObjectId(id)},
        {"$set":{'code':request.form['code']},{'name':request.form['name']},{'created_at':request.form['created_at']}})
    except Exception as e:
        return Response (dumps({'message':e}),status=404,mimetype='application/json')
@academics.route('delete<pk>',methods = ['DELETE'])
def deletesub(id):
   try:
    deletesubject = Subject.delete.one({'id':ObjectId(id)})
    return Response(dumps{'message':"id delete",'id':f'id'{id}},status=404,mimetype='application/json')
   except Exception as e:
    return Response (dumps({'message':e}),status=404,mimetype='application/json')

    
    
    
       


