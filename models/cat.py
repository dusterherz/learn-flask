from sqlalchemy import (Column, Integer, String, ARRAY)
from db import Base


class Cat(Base):
    __tablename__ = 'cats'

    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    color = Column(ARRAY(String))
