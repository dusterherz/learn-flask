from sqlalchemy import (Column, Integer, String, ARRAY, ForeignKey)
from db import Base


class Cat(Base):
    __tablename__ = 'cats'

    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    colors = Column(ARRAY(String))
    user_id = Column(Integer, ForeignKey('users.id'))
