from .models import Token, User
from flask import render_template, make_response, session, request
from functools import wraps
import os
from io import BytesIO
from xhtml2pdf import pisa
import uuid
from pathlib import Path


def token_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token, token_id = None, None
        if session and session['token']:
            token_id = session['token']
            print(token_id)
        elif 'Authorization' in request.headers:
            token_id = ((request.headers['Authorization']).split(' '))[1]
        if token_id:
            token = Token.objects(token_id=token_id).first()
        if not token:
            return {'data': 'invalid token'}
        user = User.objects(id=token.user_id.id).first()
        print(user)
        session['token'] = token_id
        session['user'] = user.to_json()
        user = token.user_id
        return f(*args, **kwargs)
    return decorated_function


def render_to_pdf2(template_src, folder_name, question_paper, params: dict):
    print(params)
    file_path = os.path.dirname(os.path.realpath(__file__))
    list = file_path.split('/')
    list.pop()
    file_path = '/'.join(list)
    # if not os.path.exists((str(file_path)+f'/media/{folder_name}/')):
    #     if not os.path.exists((str(file_path)+f'/media')):
    #         os.makedirs('media', mode=0o777)
    #     Path.mkdir(folder_name, parents=(
    #         str(file_path)+f'/media/'))
    html = render_template(
        template_src,
        data=params
    )
    folder_name = folder_name
    result = BytesIO()
    filename = str(uuid.uuid4())
    pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), result)
    exists = False

    if not question_paper:
        grade = params['grade']
        subject = params['subject']
        register_number = params['register_number']
        for file in os.listdir((str(file_path)+f'/media/{folder_name}/')):
            filename = (str(file))
            if register_number in filename:
                exists = True
        filename = f'grade-{grade}&&subject-{subject}{register_number}'
        try:
            if exists:
                os.rename((file_path+f'/media/{folder_name}/{file}'),
                          (file_path+f'/media/{folder_name}/{filename}.pdf'))
            with open(file_path+f'/media/{folder_name}/{filename}.pdf', 'wb+') as output:
                pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), output)
        except Exception as e:
            print(e)
        return filename, True
    filename = filename + '.pdf'
    pdf = pdf.text
    question_paper.file.put(pdf, encoding='utf-8', filename=filename)
    # question_paper.save()
    return question_paper, True


def get_object(model, value):
    obj = model.objects(id=value).get()
    return obj


def pagination(url, result, page, limit):
    obj = {}
    page = int(page)
    count = result.count()
    if (limit*(page-1)) > count:
        page = 1
    start = limit * (page-1)
    end = start + limit
    if count <= end:
        end = count
    else:
        obj['next'] = url + '?page={}'.format(page+1)
    if page != 1:
        obj['previous'] = url+'?page={}'.format(page-1)
    obj['result'] = (result[start:end]).to_json()
    return obj
