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
        grade = Grade(**data)
        if grade.validate():
            grade.save()
            return Response(dumps({'message': f" Grade {data['grade']} Created"}), status=200)
        return 'Not a valid grade'
    except Exception as e:
        return Response(dumps({'message': e}), status=400)
@academics.route('grade/<int:id>', methods=['PATCH', 'DELETE'])
def gradeUD(id):
    query=Grade.objects(id=id).get()
    if request.method == 'PATCH':
        print(query.to_json())
        if query:
            data=request.json
            try:
                query.update(**data)
                return Response(dumps({"message":f"Grade {query.grade} Updated "}), status=200)
            except Exception as e:
                return Response(dumps({'message':str(e)}), status=400)
    if request.method == 'DELETE':
          if query:
            try:
                query.delete()
            except Exception as e:
                return Response(dumps({'message':str(e)}), status=400)
'''Subject Creation'''
@academics.route('subject/', methods=['POST'])
def subject():
    print('POST')
    data = request.json
    query = Subject(**data)
    try:
        query.save()
        return Response(dumps({'message': f"{data['name']} Created"}), status=200)
    except Exception as e:
        return Response(dumps({'message': str(e)}), status=404)

'''Subject Update and Delete'''
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
                    query.update(**data)
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
'''Chapter creation and retrieval'''
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
            chapter = Chapter(**data,subject_id=subject)
            chapter.save()
        except Exception as e:
            return Response(dumps({'message': str(e)}))
        return Response(dumps({'message': f"{data['name']} Created"}))
    if request.method == "GET":
        chapters = Chapter.objects
        print(chapters)
        return Response(dumps({'status': 'success', 'data': chapters.to_json()}), status=200)

'''Chapter Edit and Delete '''
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

'''Chapter retrieval'''
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
'''Question Creation'''
@academics.route('question/',methods=['POST'])
def question():
    data = request.json
    query = Question(grade=data['grade'],subject=data['subject'],chapter=data['subject'],
    question=data['question'],duration=data['duration'],mark = data['mark'],chapter_no=data['chapter_no'],question_type=data['question_type'],congitive_level=data['congitive_level'],difficulty_level=data['difficulty_level'])
    # try:
    query.save()
    return Response(dumps({'staus':'created'}))
    # except Exception as e:
    #     return Response(dumps({'staus':'question is not created','data':str(e)}))    
@academics.route('instruction/',methods=['POST'])
def instructions():
    data = request.json
    try:
      instructions_query = Instruction(note=data['note'])
      if instructions_query.validate():
          instructions_query.save()
          return Response(dumps({'message':'created'}),status=200)
      return Response(dumps({"message":"sdfsf"}))     
    except Exception as e:
        return Response(dumps({'message':str(e)}),status=404)     
@academics.route('questionpaper/',methods=['POST'])
def question_paper():
    data = request.json
    query = QuestionBank(grade=data['grade'],subject=data['subject'],created_by=data['created_by'],
    created_at = data['created_at'],test_id=data['test_id'],duration=data['duration'],
    overall_mark=data['overall_mark'],no_of_question=data['no_of_question'])  
    query.save() 
    return Response(dumps({'message':'created'}),status=200) 
@academics.route('test/',methods=['POST'])
def test():
    data = request.json
    test_query = Test(question_paper=data['question_paper'],grade = data['grade'],
    subject=data['subject'],duration=data['subject'], 
    mark = data['mark'],remarks=data['remarks'],description=data['description'],
    test_id=data['test_id'],pass_percentage=data['pass_percentage'])
    test_query.save()
@academics.route('testresult/',methods=['POST'])
def testresult():
    data = request.json
    resultquery = Testresult(student_id=data['student_id'],grade=data['grade'],subject=data['subject'],test_id=data['test_id'],
    question_paper=data['question_paper'],result=data['result'],score=data['score'],correct_answer=data['correct_answer'],
    wrong_answer=data['wrong_answer'],unanswer_question=data['unanswer_question']) 
    resultquery.save()   
@academics.route('testresult<pk>/',methods=['PATCH'])
def resultupdate(id):
    testresult = Testresult.objects(id=id).first()
    if not testresult:
        return Response(dumps({'message':'not match'}))
    if request.method=="PATCH":
        data = request.json
        try:
            for x in data:
                setattr(testresult,x,data[x])
                testresult.save()
                return Response(dumps({'message':'updated'}),status=200)
        except Exception as e:
            return Response(dumps({"status":'incorrectid','data':str(e)}),status=404)    
    if request.method=='DELETE':
        testresult.delete()
        return Response(dumps({"status":"id_deleted"}),status=200)
@academics.route('questionbank/',methods=['POST'])
def questionbank():
    data = request.json
    question=Question(**data['question'])
    answer=Answer(**data['answer'],question=question)
    try:
        question.save()
        answer.save()
        return Response(dumps({'staus':'created'}))
    except Exception as e:
        return Response(dumps({'staus':'question is not created','data':str(e)}))    
@academics.route('question/<int:id>', methods=['PATCH', 'DELETE'])
def questionUD(id):
    try:
        question=Question.objects(id=id).get()
        answer=Answer.objects(question=question).get()
    except:
        return Response(dumps({'message':'Question doesn\'t exist'}))
    if question and answer:
        if request.method == 'PATCH':
            data=request.json
            try:
                question.update(**data['question'])
                answer.update(**data['answer'])
                return Response(dumps({'message':"Question updated"}))
            except Exception as e:
                return Response(dumps({"message": str(e)}),status=400)
        if request.method == 'DELETE':
            try:
                question.delete()
                answer.delete()
                return Response(dumps({'message':"Question deleted"}),status=200)
            except Exception as e:
                return Response(dumps({"message":str(e)}),status=400)
    return Response(dumps({"message":"Question doesn't exists"}),status=400)

@academics.route('load_subject_chapter',methods=['GET'])
def load_subject_chapter():
    grade_id=request.args.get('grade_id', None)
    subject_id=request.args.get('subject_id', None)
    print(grade_id,type(subject_id))
    if grade_id:
        print(grade_id)
        subject = Subject.objects(grade=int(grade_id))
        return Response(dumps({"subject":subject.to_json()}),status=200)
    chapter = Chapter.objects(subject_id=int(subject_id))
    return Response(dumps({"chapter":chapter}),status=200)
@academics.route('load_grade',methods=['GET'])
def load_grade():
    user = 'is_admin'
    if user.usertype == 'is_admin':
        grades = Grade.objects
        return Response(dumps({"data":grades.to_json()}),status=200)
    elif user.user_type == 'is_staff':
        standard = user.profile.standard
        grades = Grade.objects(grade=standard)
        return Response(dumps({"data":grades.to_json()}),status=200)
    else:
        return None
# @academics.route('load_test',methods=['GET'])
# def load_test(request):
#     # grade_id = request.GET.get('grade', None)
#     subject_id = request.GET.get('subject', None)
#     if subject_id:
#         test = Test.objects.filter(subject_id= subject_id)
#     return render(request, 'academics/test_dropdown.html', {'items':test})
# @academics.route('load_chapter',methods=['GET'])
# def load_chapter_no(request):
#     subject_id = request.GET.get('subject', None)
#     chapter = Chapter.objects.filter(subject=subject_id)
#     return render(request, 'academics/dropdown_chapter_no.html', {'items': chapter})
