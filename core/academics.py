from flask import Blueprint, request, Response, jsonify
from json import dumps, loads
from .models import *


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
@academics.route('subject/',methods=['POST'])  
def sub():
    data = request.json
    try:
        subject = Subject(name=data['name'],grade=data['grade'],
        code=data['code'],created_at=data['created_at']) 
        subject.save()
        return Response(dumps({'message':f"Subject{data['code']}created"}),status=200)
    except Exception as e:
        return Response(dumps({'message':e}),status=404) 
@academics.route('update<pk>/',methods = ['PATCH','DELETE'])
def updatedsub(id):
    subject = Subject.objects(id=int(id))
    if request.methods == 'PATCH':
        data = request.json
        subject.update(name=data['name'],code = data['code'],created_at = data['created_at'])
        return Response(dumps({'message':'sucessfull','data':subject.to_json()}),status=200)
    elif request.methods =='DELETE':
        subject.delete()
    return Response(dumps({'message':'deleted'}),status=200)
@academics.route('question/',methods =['POST']) 
def question():
    data=request.json
    try:
        questions = Question(grade=data['grade'],subject=data['subjects'],chapter=data['chapter'],
        question=data['question'],mark=data['mark'],
        chapter_no=data['chapter_no'],question_type=data['question_type'])
        if questions.validate():
            questions.save()
            return Response(dumps({'message':'created'}),status=200)
    except Exception as e:
        return Response(dumps({'message':e}),status=400)
@academics.route('update<pk>/',methods=['PATCH','DELETE'])        
def updatequestion(id):
    question = Question.object(id=int(id))
    if request.methods == 'PATCH':
        data = request.json
        question.update(grade=data['grade'],subject=data['subjects'],chapter=data['chapter'],
        question=data['question'],duration=data['duration'],mark=data['mark'],
        chapter_no=data['chapter_no'],created_at=data['created_at'],question_type=data['question_type'])
        return Response(dumps({'message':'updated','data':question.to_json()}),status=200)
    elif  request.methods =='DELETE':
        question.delete()
        return Response(dumps({'message':'deleted'}),status=200)



















#     data = request.json
#     try:
#         subjets = Subject.update.one({'id':ObjectId(id)},
#         {"$set":{'code':request.form['code']},{'name':request.form['name']},{'created_at':request.form['created_at']}})
#     except Exception as e:
#         return Response (dumps({'message':e}),status=404,mimetype='application/json')
# @academics.route('delete<pk>',methods = ['DELETE'])
# def deletesub(id):
#    try:
#     deletesubject = Subject.delete.one({'id':ObjectId(id)})
#     return Response(dumps{'message':"id delete",'id':f'id'{id}},status=404,mimetype='application/json')
#    except Exception as e:
#     return Response (dumps({'message':e}),status=404,mimetype='application/json')

    
    
    
       


