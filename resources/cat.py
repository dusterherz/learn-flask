from flask_restful import (reqparse, Resource, fields, marshal_with, abort)

from models import Cat
from db import session
from auth import auth

cat_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'colors': fields.List(fields.String)
}

cat_parser = reqparse.RequestParser()
cat_parser.add_argument('name', type=str)
cat_parser.add_argument('colors', type=str, action='append')


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
        if (parsed_args['colords']):
            cat.colors = parsed_args['colors']
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
