from flask_restful import (reqparse, Resource, fields, marshal_with, abort)

from models import Cat, User
from db import session
from auth import auth

cat_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'colors': fields.List(fields.String),
    'user_id': fields.Integer
}

cat_parser = reqparse.RequestParser()
cat_parser.add_argument('name', type=str, default="Minet")
cat_parser.add_argument('colors', type=str, action='append', default=[])
cat_parser.add_argument('user_id', type=int)


class CatResource(Resource):
    decorators = [auth.login_required]

    @marshal_with(cat_fields)
    def get(self, id):
        cat = session.query(Cat).get(id)
        if not cat:
            abort(404, message="Cat {} does not exist".format(id))
        return cat

    @marshal_with(cat_fields)
    def post(self, id):
        parsed_args = cat_parser.parse_args()
        cat = session.query(Cat).get(id)
        if not cat:
            abort(404, message="Cat {} does not exist".format(id))
        if (parsed_args['name']):
            cat.name = parsed_args['name']
        if (parsed_args['colors']):
            cat.colors = parsed_args['colors']
        if (parsed_args['user_id']):
            user = session.query(User).get(parsed_args['user_id'])
            if not user:
                abort(404, message="User {} does not exist".format(
                    parsed_args['user_id']))
            cat.owner = user
        session.add(cat)
        session.commit()
        return cat

    @marshal_with(cat_fields)
    def delete(self, id):
        cat = session.query(Cat).get(id)
        if not cat:
            abort(404, message="Cat {} does not exist".format(id))
        session.delete(cat)
        session.commit()
        return cat


class CatListResource(Resource):
    decorators = [auth.login_required]

    @marshal_with(cat_fields)
    def get(self):
        cats = session.query(Cat).all()
        return cats

    @marshal_with(cat_fields)
    def post(self):
        parsed_args = cat_parser.parse_args()
        cat = Cat(**parsed_args)
        session.add(cat)
        session.commit()
        return cat
