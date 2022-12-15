from flask import Blueprint, request, Response, jsonify, session, render_template
from json import dumps, loads
from .models import *
from .utils import token_required, render_to_pdf2, get_object, pagination
from .models import Chapter
import random
from bson import json_util
from mongoengine import connect, get_db
# from flask_paginate import get_parameter, get_page_parameter, Pagination
# from flask_rest_paginate import Pagination
# from . import pagination
from .accounts import db

# connect(
#     host='mongodb+srv://root:12345@cluster0.kv3gwol.mongodb.net/school'
# )
# db = get_db()

# pagination = Pagination(db=db)
academics = Blueprint('academics', __name__)

models = {
    'grade': Grade, 'subject': Subject, 'chapter': Chapter, 'question_paper': Question_paper, 'test': Test, 'test_result': Testresult}

# grade


@academics.route('grade/', methods=['GET', 'POST'])
def grade():
    user = None
    if 'user' in session:
        user = loads(session['user'])
        print(user)
    if request.method == 'GET':
        grades = Grade.objects
        page = request.args.get('page')
        if user:
            profile = Profile.objects(user=user['_id']).get()
            if user['usertype'] == 'is-staff':
                grade = profile.standard
                # print(pagination)
                # print(grade, type(grade))
                grade_list = []
                for i in grade:
                    grade_list.append(int((i.split('-'))[0]))
                # print(grade_list)
                grades = grades(grade__in=grade_list)

            if user['usertype'] == 'is_student':
                return Response({"status": "failure", 'data': 'Your not have access to view this page'})
        if page:
            grades = pagination('http://127.0.0.0:7000/grade',
                                grades, page, 2)
        else:
            grades = grades.to_json()
        # page = request.args.get(get_page_parameter(), type=int, default=1)
        # grades = pagination.paginate(grades, Grade)
        # grades = grades.paginate(page=1, per_page=10)
        return Response(dumps({'status': 'success', 'data': grades}), status=200)
    if request.method == 'POST':
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
    query = Grade.objects(id=id).get()
    if request.method == 'PATCH':
        print(query.to_json())
        if query:
            data = request.json
            try:
                query.update(**data)
                return Response(dumps({"message": f"Grade {query.grade} Updated "}), status=200)
            except Exception as e:
                return Response(dumps({'message': str(e)}), status=400)
    if request.method == 'DELETE':
        if query:
            try:
                query.delete()
            except Exception as e:
                return Response(dumps({'message': str(e)}), status=400)


'''Subject Creation'''


@academics.route('subject/', methods=['POST', 'GET'])
def subject():
    if request.method == 'POST':
        data = request.json
        query = Subject(**data)
        try:
            query.save()
            return Response(dumps({'message': f"{data['name']} Created"}), status=200)
        except Exception as e:
            return Response(dumps({'message': str(e)}), status=404)
    queryset = Subject.objects
    grade = request.args.get('grade')
    if grade is not None:
        try:
            grades = Grade.objects(grade=grade).first()
            queryset = queryset(grade_id=grades.id)
            data = queryset.to_json()
            print(data)
            if len(queryset) > 0:
                return Response(dumps({'status': 'success', "data": data}), status=200)
            return Response(dumps({"status": f"No Subject for this grade {grade}"}), status=206)

        except:
            return Response(dumps({'status': 'failed'}), status=206)
    return Response(dumps({"status": "success", "data": queryset.to_json()}), status=200)


'''Subject Update and Delete'''


@academics.route('subject/<int:id>', methods=['GET', 'PATCH', 'DELETE'])
def subjectUD(id=None):
    try:
        query = get_object(Subject, id)
    except Exception as e:
        return Response(dumps({'message': str(e)}), status=400)
    if request.method == 'PATCH':
        data = request.json
        query = Subject.objects(id=int(id)).first()
        print(query.to_json())
        if query:
            try:
                code = Subject.objects(code=str(data['code'])).first()
                if code is None or code.id == id:
                    query.update(**data)
                    return Response(dumps({'message': f" From Standard {str(query.grade_id.grade)},Subject {query.name} updated to {data['name']} "}), status=400)
                else:
                    return Response(dumps({'message': f' {code.name} Subject code already exists'}), status=404)
            except Exception as e:
                print(e)
                return Response(dumps({'message': str(e)}), status=400)
    if request.method == 'DELETE':
        query.delete()
        return Response(dumps({'status': 'success', "data": f"chapter {subject.name} deleted successfully"}))
    return Response(dumps({'status': 'success', 'data': query.to_json()}))


'''Chapter creation and retrieval'''


@academics.route('chapter/', methods=['GET', 'POST'])
# @token_required
def chapter():
    if request.method == "POST":
        data = request.json
        print(data)
        try:
            subject = get_object(Subject, data['subject'])
            print(subject)
            chapter = Chapter(**data, subject=subject)
            chapter.save()
        except Exception as e:
            return Response(dumps({'message': str(e)}))
        return Response(dumps({'message': f"{data['name']} Created"}))
    if request.method == "GET":
        chapters = Chapter.objects
        print(chapters)
        return Response(dumps({'status': 'success', 'data': chapters.to_json()}), status=200)


'''Chapter Edit and Delete '''


@ academics.route('chapter/<id>/', methods=['GET', 'PATCH', "DELETE"])
def chapter_edit(id):
    try:
        chapter = get_object(Chapter, id)
    except Exception as e:
        return Response(dumps({'message': str(e)}))
    if request.method == "PATCH":
        data = request.json
        print(data)
        try:
            for key in data:
                if key == 'subject':
                    data['subject'] = get_object(Subject, data['subject'])
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
    return Response(dumps({'status': 'success', 'data': chapter.to_json()}))


'''Chapter retrieval'''


@ academics.route('chapter-list', methods=['POST'])
def chapter_list():
    try:
        data = request.json
        grade = Grade.objects(grade=data['grade']).get()
        subject = Subject.objects(grade=str(grade.id),
                                  name=data['subject']).get()
        chapters = Chapter.objects(subject=subject)
        if not len(chapters):
            return Response(dumps({'status': 'failure', 'data': "subject doesn't have chapters"}))
        chapters = loads(chapters.to_json())
        for chapter in chapters:
            chapter['grade'] = grade.grade
            chapter['subject'] = subject.name
            chapter['subject_id'] = subject.id
    except Exception as e:
        return Response(dumps({"status": "failure", "data": str(e)}), status=206)
    return Response(dumps({'status': 'success', 'data': chapters}))


'''Question Creation'''


@academics.route('question/', methods=['GET', 'POST'])
def question():
    if request.method == 'GET':
        grade = request.args.get('grade')
        subject = request.args.get('subject')
        from_chapter_no = request.args.get('from_chapter_no')
        to_chapter_no = request.args.get('to_chapter_no')
        questions = Question.objects
        q = Question.objects(question="what is science").first()
        try:
            if grade and subject:
                questions = questions(grade=grade, subject=subject)
                if from_chapter_no and to_chapter_no:
                    questions = questions(
                        chapter_no__gte=from_chapter_no, chapter_no__lte=to_chapter_no)
            page = request.args.get('page')
            if page:
                questions = pagination('http://127.0.0.0:7000/question',
                                       questions, page, 2)
            else:
                questions = questions.to_json()
            return Response(dumps({"status": "success", 'data': questions}), status=200)
        except Exception as e:
            return Response(dumps({'status': 'failure', 'data': str(e)}))
    if request.method == 'POST':
        data = request.json
        try:
            data['question']['grade'] = get_object(
                Grade, data['question']['grade'])
            data['question']['subject'] = get_object(
                Subject, data['question']['subject'])
            data['question']['chapter'] = get_object(
                Chapter, data['question']['chapter'])
            question = Question(**data['question'])
            answer = Answer(**data['answer'], question=question)
            question.save()
            answer.save()
            return Response(dumps({'staus': 'created'}))
        except Exception as e:
            return Response(dumps({'status': 'question is not created', 'data': str(e)}))

# question edit


@academics.route('question/<int:id>', methods=['PATCH', 'DELETE'])
def questionUD(id):
    try:
        question = get_object(Question, id)
        answer = Answer.objects(question=question).get()
    except Exception as e:
        return Response(dumps({'message': str(e)}))
    if question and answer:
        if request.method == 'PATCH':
            data = request.json
            try:
                question.update(**data['question'])
                answer.update(**data['answer'])
                return Response(dumps({'message': "Question updated"}))
            except Exception as e:
                return Response(dumps({"message": str(e)}), status=400)
        if request.method == 'DELETE':
            try:
                question.delete()
                answer.delete()
                return Response(dumps({'message': "Question deleted"}), status=200)
            except Exception as e:
                return Response(dumps({"message": str(e)}), status=400)
    return Response(dumps({"message": "Question doesn't exists"}), status=400)

# load chapter,subject


@academics.route('load_subject_chapter', methods=['GET'])
def load_subject_chapter():
    grade_id = request.args.get('grade_id', None)
    subject_id = request.args.get('subject_id', None)
    print(grade_id, type(subject_id))
    if grade_id:
        print(grade_id)
        subject = Subject.objects(grade=int(grade_id))
        print(subject)
        return render_template('dropdown_list_options.html', items=list(subject))
    chapter = list(Chapter.objects(subject_id=int(subject_id)))
    return render_template('dropdown_list_options.html', items=chapter)

# load grade


@academics.route('load_grade', methods=['GET'])
def load_grade():
    user = loads(session['user'])
    if user['usertype'] == 'is_admin':
        grades = Grade.objects
    elif user['usertype'] == 'is_staff':
        standard = user.profile.standard
        grades = Grade.objects(grade=standard)
    else:
        return None
    return render_template('dropdown_grade.html', items=list(grades))

# load test


@academics.route('load_test', methods=['GET'])
def load_test(request):
    subject_id = request.args.get('subject')
    if subject_id:
        test = Test.objects(subject=subject_id)
    return render_template('test_dropdown.html', items=list(test))

# load chapter no


@academics.route('load_chapter', methods=['GET'])
def load_chapter_no(request):
    subject_id = request.GET.get('subject', None)
    chapter = Chapter.objects(subject_id=subject_id)
    return render_template('dropdown_chapter_no.html', items=list(chapter))

# question paper create


@ academics.route('question-list', methods=['GET', 'POST'])
def question_list():
    if request.method == 'GET':
        grade = request.args.get('grade')
        subject = request.args.get('subject')
        question_papers = Question_paper.objects
        try:
            if grade:
                grade_obj = Grade.objects(grade=grade).get()
                question_papers = question_papers(grade=grade_obj.id)
                if subject:
                    subject = subject.upper()
                    subject_obj = Subject.objects(
                        grade=grade_obj.id, name=subject).get()
                    question_papers = question_papers(
                        subject=subject_obj.id)
            page = request.args.get('page')
            if page:
                question_papers = pagination('http://127.0.0.0:7000/question-list',
                                             question_papers, page, 2)
            else:
                question_papers = question_papers.to_json()
            return Response(dumps({'status': 'success', 'data': question_papers}), status=200)
        except Exception as e:
            return Response(dumps({"status": "failure", "data": str(e)}), status=206)

    if request.method == 'POST':
        save_obj = request.args.get('type')
        try:
            data = request.json
            if 'timing' in data:
                data['timing'] = int(data['timing'])
            if 'overall_marks' in data:
                data['overall_marks'] = int(data['overall_marks'])
            grade = Grade.objects(grade=data['grade']).get()
            subject = get_object(Subject, data['subject'])
            user = loads(session['user'])
            questions = []
            if 'customize' in data and data['customize']:
                customize = data['customize']
                for i in customize:
                    chapter = Chapter.objects(id=i['id']).get()
                    for j in i['cognitive_level']:
                        try:
                            # cognitive = j.capitalize()
                            newlist = Question.objects(
                                chapter=chapter.id, congitive_level=j)
                            newlist = (
                                sorted(newlist, key=lambda x: random.random()))
                            num = int(i['cognitive_level'][j])
                            if len(newlist) >= num:
                                newlist = newlist[:num]
                                questions.append(newlist)
                            else:
                                return Response(dumps({'status': 'failure', 'data': ('Required questions not available in {} level in chapter {}. Available number of questions is {}').format(j, chapter, len(newlist))}), status=206)
                        except Exception as e:
                            return Response(dumps({"status": "failure", "data": str(e)}), status=206)
                questions = [item for sublist in questions for item in sublist]
                print(questions)
            else:
                if 'question_list' in data:
                    list_of_questions = data['question_list']
                else:
                    return Response(dumps({'status': 'failure', 'data': "question_list is not given"}))
                if save_obj:
                    save_obj = save_obj.lower()
                for i in list_of_questions:
                    j = Question.objects(id=i).first()
                    if j:
                        print(j)
                        questions.append(j)
                # answers
            answers = []
            question_list = []
            for question in questions:
                answer_obj = Answer.objects(id=question.answer).first()
                ans = getattr(answer_obj, str(answer_obj.correctanswer))
                question_list.append(question.question)
                answers.append(ans)
            print(question_list, answers)
            context = {'data': question_list, 'grade': grade.grade,
                       'subject': subject.name, 'register_number': user['registernumber']}
            context1 = {'data': question_list, 'grade': grade.grade,
                        'subject': subject.name, 'register_number': user['registernumber'], 'answers': answers}
            answer_file, status = render_to_pdf2(
                'answer_file.html', 'answer_files', None, context1)
            #     # save question_paper in data_base
            print(answer_file)
            if save_obj == 'save':
                cal_timing = 0
                cal_overall_marks = 0
                for i in questions:
                    print(int(i.duration))
                    cal_timing += int(i.duration)
                    cal_overall_marks += int(i.mark)
                if not data['timing']:
                    data['timing'] = cal_timing
                if not data['overall_marks']:
                    data['overall_marks'] = cal_overall_marks
                created_by = user['email']
                question_paper = Question_paper(
                    grade=grade, subject=subject, created_by=created_by, timing=data['timing'], overall_marks=data['overall_marks'])
                # question_paper.save()
                # print(question_paper.to_json)
        #         print(question_paper)
                question_id_list = []
                for question in questions:
                    question_id_list.append(question.id)
                question_paper.question_list = question_id_list
                for i in range(0, len(questions)):
                    questions[i] = questions[i].to_json()
                question_paper, status = render_to_pdf2(
                    'question.html', 'question_files', question_paper, context)
                question_paper.save()
                print(type(question_paper))
                if not status:
                    return Response({"status": "failure", "data": "given details are incorrect"}, status=206)
                return Response(dumps({'status': 'success', 'data': question_paper.to_json(), 'question_details': questions, 'questions': question_list, 'answer-file-path': '/media/answer_files/{answer_file}.pdf', 'subject_id': subject.id, 'grade_id': grade.id}), status=200)
            filename, status = render_to_pdf2(
                'question.html', 'question_papers', None, context)
            if not status:
                return Response({"status": "failure", "data": "given details are incorrect"}, status=206)
            return Response(dumps({'status': 'success', 'question_path': f'/media/question_paper/{filename}.pdf', 'answer_path': f'/media/answer_files/{answer_file}.pdf', 'subject_id': subject.id, 'grade_id': grade.id}), status=200)
        except Exception as e:
            return Response(dumps({"status": "failure", "data": str(e)}), status=206)

# question paper edit


@ academics.route('question-paper/<id>/', methods=['GET', 'PATCH', "DELETE"])
def question_paper_edit(id):
    try:
        question_paper = get_object(Question_paper, id)
    except Exception as e:
        return Response(dumps({'message': str(e)}))
    if request.method == "PATCH":
        data = request.json
        print(data)
        try:
            for key in data:
                print(key)
                setattr(question_paper, key, data[key])
            question_paper.save()
            print(question_paper)
        except Exception as e:
            print(str(e))
            return Response(dumps({'status': 'failure', 'data': str(e)}))
        return Response(dumps({'status': 'success', 'data': question_paper.to_json()}))
    if request.method == "DELETE":
        question_paper.delete()
        return Response(dumps({'status': 'success', 'data': 'question paper deleted successfully'}))
    return Response(dumps({'status': 'success', 'data': question_paper.to_json()}))

# retrive questions from question paper


@ academics.route('test-questions', methods=['GET'])
def question_from_question_paper():
    try:
        question_paper_id = request.args.get('question_paper')
        question_paper = get_object(Question_paper, question_paper_id)
    except Exception as e:
        return Response(dumps({'message': 'give a valid question paper id'}))
    question_list = question_paper.question_list
    data = []
    change = False
    # print(question_list, type(question_list))
    try:
        for id in list(question_list):
            pipeline = [{"$match": {"_id": id}}, {"$lookup": {
                "from": "answer",
                "localField": "answer",
                "foreignField": "_id",
                "as": "answer"
            }}]
            question = list(Question.objects.aggregate(
                pipeline=pipeline))[0]
            print(question)
            if question:
                data.append(json_util.dumps(question))
            else:
                question_list.remove(id)
                change = True
        if change:
            question_paper.question_list = question_list
            question_paper.save()
    except Exception as e:
        return Response(dumps({'message': str(e)}))
    return Response(dumps({'status': 'success', 'data': data}), status=200)

# test create


@ academics.route('test/', methods=['GET', 'POST'])
def test():
    user = loads(session['user'])
    if request.method == 'GET':
        grade = request.args.get('grade')
        test_uid = request.args.get('test_uid')
        test = Test.objects
        try:
            if grade:
                grade_obj = Grade.objects(grade=grade).first()
                test = test(grade=grade_obj.id)
            if test_uid:
                test = test(test_uid=test_uid).first()
                return Response(dumps({"status": "success", 'data': test.to_json()}), status=200)
            page = request.args.get('page')
            if page:
                test = pagination('http://127.0.0.0:7000/test',
                                  test, page, 2)
            else:
                test = test.to_json()
            return Response(dumps({"status": "success", 'data': test}), status=200)
        except Exception as e:
            return Response(dumps({"status": "failure", "data": str(e)}), status=206)
    if request.method == 'POST':
        try:
            data = request.json
            data['grade'] = get_object(Grade, data['grade'])
            data['subject'] = get_object(Subject, data['subject'])
            data['created_staff_id'] = User.objects(
                id=user['_id'], usertype__ne='is_student').get()
            data['question_paper'] = get_object(
                Question_paper, data['question_paper'])
            test_query = Test(**data)
            question_paper = data['question_paper']
            test_query.save()
            test = Test.objects(question_paper=question_paper).get()
            question_paper.test_uid = test.test_uid
            # question_paper.save()
        except Exception as e:
            return Response(dumps({"status": "failure", "data": str(e)}), status=206)
        return Response(dumps({"status": "success", 'data': test_query.to_json()}), status=201)

# test edit


@ academics.route('test/<id>', methods=['GET', 'PATCH', 'DELETE'])
def test_edit(id):
    test = Test.objects(id=id).first()
    if not test:
        return Response(dumps({'status': 'failure', 'data': "test doesn't exists"}))
    if request.method == 'PATCH':
        data = request.json
        # try:
        for key in data:
            if key == 'question_paper' or key == 'grade' or key == 'subject':
                print(key, models[key])
                data[key] = get_object(models, data[key])
            print(data[key])
            setattr(test, key, data[key])
        test.save()
        # except Exception as e:
        #     return Response(dumps({'message': 'incorrect', 'data': str(e)}), status=206)
        return Response(dumps({'message': 'success', 'data': test.to_json()}), status=200)
    if request.mehtod == 'DELETE':
        test_uid = test.test_uid
        question_paper = Question_paper.objects(test_uid=test_uid).first()
        if question_paper:
            question_paper.test_uid = None
            question_paper.save()
        test.delete()
        return Response(dumps({'message': 'deleted'}), status=202)

# test result


@ academics.route('testresult/', methods=['GET', 'POST'])
def test_result():
    user = loads(session['user'])
    if request.method == 'GET':
        grade = request.args.get('grade')
        test_id = request.args.get('test_id')
        student_id = request.args.get('student_id')
        test_result = Testresult.objects

        try:
            if grade:
                grade_obj = Grade.objects(grade=grade).get()
                test_result = test_result(grade=grade_obj.id)
            if test_id:
                test_result = test_result(test_id=test_id).get()
                return Response(dumps({'status': 'success', 'data': test_result.to_json()}), status=200)
            if student_id:
                student = User.objects(
                    id=student_id, usertype='is_student').get()
                test_result = test_result(student_id=student.id)
            page = request.args.get('page')
            if page:
                test_result = pagination('http://127.0.0.0:7000/testresult',
                                         test_result, page, 2)
            else:
                test_result = test_result.to_json()
            return Response(dumps({"status": "success", 'data': test_result}), status=200)
        except Exception as e:
            return Response(dumps({'status': 'success', 'data': str(e)}), status=206)

    if request.method == 'POST':
        try:
            data = request.json
            data['grade'] = get_object(Grade, data['grade'])
            data['subject'] = get_object(Subject, data['subject'])
            data['question_paper'] = get_object(
                Question_paper, data['question_paper'])
            data['student_id'] = User.objects(
                id=user['_id'], usertype='is_student').get()
            data['test_id'] = get_object(Test, data['test_id'])
            resultquery = Testresult(student_id=data['student_id'], grade=data['grade'], subject=data['subject'], test_id=data['test_id'],
                                     question_paper=data['question_paper'], result=data['result'], score=data[
                'score'], correct_answer=data['correct_answer'],
                wrong_answer=data['wrong_answer'], unanswer_question=data['unanswer_question'], test_details=data['test_details'])
            resultquery.save()
        except Exception as e:
            return Response(dumps({"status": "failure", "data": str(e)}), status=206)
        return Response(dumps({"status": "success", 'data': resultquery.to_json()}), status=201)

# test result edit


@ academics.route('testresult/<id>', methods=['PATCH'])
def resultupdate(id):
    testresult = Testresult.objects(id=id).first()
    if not testresult:
        return Response(dumps({'status': 'failure', 'data': "test result dosn't exists"}))
    if request.method == "PATCH":
        data = request.json
        try:
            for key in data:
                setattr(testresult, key, data[key])
                testresult.save()
                return Response(dumps({'status': 'success', 'data': testresult.to_json()}), status=200)
        except Exception as e:
            return Response(dumps({"status": 'failure', 'data': str(e)}), status=206)
    if request.method == 'DELETE':
        testresult.delete()
        return Response(dumps({"status": "success", 'data': 'deleted'}), status=200)
