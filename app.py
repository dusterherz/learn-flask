from flask import Flask
from flask_restful import Api

from resources import (CatResource, CatListResource,
                       LoginResource, SignupResource)
import settings

app = Flask(__name__)
api = Api(app)

api.add_resource(LoginResource, '/api/v1/auth/login', endpoint='login')
api.add_resource(SignupResource, '/api/v1/auth/signup', endpoint='signup')
api.add_resource(CatListResource, '/api/v1/cats/', endpoint='cats')
api.add_resource(CatResource, '/api/v1/cats/<int:id>', endpoint='cat')

if __name__ == '__main__':
    app.run(debug=settings.DEBUG)
