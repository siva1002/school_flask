from flask import Blueprint, request, Response, jsonify
from json import dumps, loads
from .models import *
from .utils import token_required, render_to_pdf2
from .models import Chapter
from flask import session
import random
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


@academics.route('question-list', methods=['POST'])
def question_list():
    type = request.args.get('type')
    data = request.json
    if 'timing' in data:
        data['timing'] = int(data['timing'])
    if 'overall_marks' in data:
        data['overall_marks'] = int(data['overall_marks'])
    print(data['timing'], data['overall_marks'])
    question_details_list = []
    list_of_questions = data['list_of_questions']
    grade = Grade.objects(grade=data['grade']).first()
    if not grade:
        return Response(dumps({'status': 'failure', 'data': "grade doesn't exists"}))
    subject = Subject.objects(id=data['subject']).first()
    if not subject:
        return Response(dumps({'status': 'failure', 'data': "subject doesn't exists"}))
    # try:
    user = loads(session['user'])
    questions = []
    if 'customized' in data and data['customize']:
        customize = data['customize']
        for i in customize:
            chapter = Chapter.objects(id=i['id'])
            for j in i['cognitive_level']:
                try:
                    cognitive = j.copitalize()
                    newlist = Question.object(
                        chapter=chapter.id, cognitive_level=cognitive)
                    newlist = (sorted(newlist, key=lambda x: random.random()))
                    num = int(i['cognitive_level'][j])
                    if len(newlist) >= num:
                        newlist = newlist[:num]
                        questions.append(newlist)
                    else:
                        return Response(dumps({'status': 'failure', 'data': ('Required questions not available in {} level in chapter {}. Available number of questions is {}').format(cognitive, chapter, len(newlist))}), status=206)
                except Exception as e:
                    return Response({"status": "failure", "data": "given details are incorrect"}, status=206)
        questions = [item for sublist in questions for item in sublist]
    else:
        if type:
            type = type.lower()
        for i in list_of_questions:
            # try:
            j = Question.objects(id=i).first()
            print(j)
            questions.append(j)
            # except:
            # continue
    #     # answers
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
        # answer_file, status = render_to_pdf2(
        #     'academics/answer_file.html', 'answer_files', None, context1)
    #     # save question_paper in data_base
        if type == 'save':
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

            question_paper = Question_paper(grade=grade, subject=subject, created_by=created_by,
                                            question_list=list_of_questions, timing=data['timing'], overall_marks=data['overall_marks'])
            question_paper.save()
            print(question_paper.to_json)
    #         print(question_paper)
    #         for question in questions:
    #             question_paper.no_of_questions.append(question.id)
    #         question_paper, status = render_to_pdf2(
    #             'academics/question.html', 'question_files', question_paper, context)
    #         if not status:
    #             return Response({"status": "failure", "data": "given details are incorrect"}, status=HTTP_206_PARTIAL_CONTENT)
    #         serializer = QuestionPaperSerializer(question_paper)
    #         return Response({'status':'success','data':serializer.data,'question_details':serializer_for_questions.data,'questions':question_list,'answer-file-path':'/media/answer_files/{answer_file}.pdf','subject_id':subject_obj.id,'grade_id':grade.id},status=HTTP_200_OK)
    #     filename,status = render_to_pdf2('academics/question.html','question_paper',None,context)
    #     if not status:
    #         return Response({"status": "failure", "data": "given details are incorrect"}, status=HTTP_206_PARTIAL_CONTENT)
    #     return Response({'status': 'success', 'question_path': f'/media/question_paper/{filename}.pdf', 'answer_path': f'/media/answer_files/{answer_file}.pdf', 'subject_id': subject_obj.id, 'grade_id': grade.id})
    # except:
    #     return Response({"status": "failure", "data": "given details are incorrect"}, status=HTTP_206_PARTIAL_CONTENT)
    return 'done'
