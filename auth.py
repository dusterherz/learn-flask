from flask_httpauth import HTTPBasicAuth
from flask import g

from models import User

auth = HTTPBasicAuth()


@auth.verify_password
def verify_token(token, password):
    user = User.verify_auth_token(token)
    if not user:
        return False
    g.user = user
    return True
