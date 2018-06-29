import os

DB_URI = os.environ.get('DB_URI')
SECRET_KEY = os.environ.get('SECRET_KEY')
DEBUG = True if os.environ.get('ENV') == 'dev' else False
