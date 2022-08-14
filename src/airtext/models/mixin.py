from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from airtext.config import MESSAGES_DATABASE_URL

Base = declarative_base()
metadata = Base.metadata


class DatabaseMixin:
    def __init__(self):
        engine = create_engine(url=MESSAGES_DATABASE_URL)
        self.session = sessionmaker(engine)
