from sqlalchemy import (Column, Integer, String)
from sqlalchemy.orm import relationship
from passlib.hash import bcrypt
from itsdangerous import (
    TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired)

from settings import SECRET_KEY
from db import Base, session


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    email = Column(String(255), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    username = Column(String(255), unique=True, nullable=False)
    cats = relationship('Cat', backref='owner')

    def __init__(self, email, password, username):
        self.email = email
        self.username = username
        self.password = bcrypt.hash(password)

    def verify_password(self, password):
        return bcrypt.verify(password, self.password)

    def generate_auth_token(self, expiration=600):
        serializer = Serializer(SECRET_KEY, expires_in=expiration)
        return serializer.dumps({'id': self.id})

    @staticmethod
    def verify_auth_token(token):
        serializer = Serializer(SECRET_KEY)
        try:
            data = serializer.loads(token)
        except SignatureExpired:
            return None
        except BadSignature:
            return None
        user = session.query(User).get(data['id'])
        return user
