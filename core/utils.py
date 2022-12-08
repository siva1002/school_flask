from .models import Token, User
from flask import session, request
from functools import wraps


def token_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session and session['token']:
            token_id = session['token']
            print(token_id)
        else:
            token_id = ((request.headers['Authorization']).split(' '))[1]
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
