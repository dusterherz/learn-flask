from flask_restful import (reqparse, Resource, fields, marshal_with, abort)
from sqlalchemy.exc import IntegrityError

from db import session
from models import User

login_fields = {
    'token': fields.String,
}

login_parser = reqparse.RequestParser()
login_parser.add_argument('email', type=str, required=True)
login_parser.add_argument('password', type=str, required=True)

signup_fields = {
    'username': fields.String,
    'email': fields.String,
}

signup_parser = login_parser.copy()
signup_parser.add_argument('username', type=str, required=True)


class LoginResource(Resource):

    @marshal_with(login_fields)
    def post(self):
        parsed_args = login_parser.parse_args()
        user = session.query(User).filter_by(email=parsed_args['email']).first()
        if not user:
            abort(401, message="The email or the password is incorrect")
        if not user.verify_password(parsed_args['password']):
            abort(401, message="The email or the password is incorrect")
        token = user.generate_auth_token()
        return {'token': token.decode('UTF-8')}


class SignupResource(Resource):

    @marshal_with(signup_fields)
    def post(self):
        parsed_args = signup_parser.parse_args()
        try:
            user = User(**parsed_args)
            session.add(user)
            session.commit()
        except IntegrityError:
            abort(409, message="Email is already used")
        return {'username': user.username, 'email': user.email}
