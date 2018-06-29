from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import (scoped_session, sessionmaker)
from settings import DB_URI
from models import *

Session = sessionmaker(autocommit=False, autoflush=False,
                       bind=create_engine(DB_URI))
session = scoped_session(Session)
Base = declarative_base()

if __name__ == '__main__':
    from sqlalchemy import create_engine
    from db import Base

    engine = create_engine(DB_URI)
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
