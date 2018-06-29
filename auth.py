from flask_httpauth import HTTPTokenAuth
from flask import g

from models import User

auth = HTTPTokenAuth()


@auth.verify_token
def verify_token(token):
    user = User.verify_auth_token(token)
    if not user:
        return False
    g.user = user
    return True
