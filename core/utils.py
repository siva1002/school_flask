from .models import Token, User
from flask import render_template,make_response,session,request
from functools import wraps
import os
import pdfkit

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
    file_path = os.path.dirname(os.path.realpath(__file__))
    list = file_path.split('/')
    list.pop()
    file_path = '/'.join(list)
    # print(file_path)
    html = render_template(
        template_src,
        params=params
    )

    # return 
    # print(questionb)
    # template = get_template(template_src)
    folder_name = folder_name
    # html = template.render(params)
    # result = BytesIO()
    # filename = str(uuid.uuid4())
    # pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), result)
    # exists = False

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
                os.rename((file_path+f'/media/{folder_name}/{file}'), (file_path+f'/media/{folder_name}/{filename}.pdf'))
            with open(file_path+f'/media/{folder_name}/{filename}.pdf', 'wb+') as output:
                # pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), output)
                response = make_response(html,False)
                response.headers["Content-Type"] = "application/pdf"
        except Exception as e:
            print(e)
        return filename, True
    # questionfile = SimpleUploadedFile(
    #     filename+'.pdf', result.getvalue(), content_type='application/pdf')
    # print(questionfile)
    # question_paper.file = questionfile
    # question_paper.save()
    # return question_paper, True


# def index():
#     name = "SIR JOHN WILLIAMSON LATHAM"
#     html = render_template(
#         "certificate.html",
#         name=name)
#     pdf = pdfkit.from_string(html, False)
#     response = make_response(pdf)
#     response.headers["Content-Type"] = "application/pdf"
#     response.headers["Content-Disposition"] = "inline; filename=output.pdf"
#     return response
