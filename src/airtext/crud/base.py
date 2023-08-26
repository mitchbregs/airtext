from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from airtext.config import AIRTEXT_DATABASE_URL


class DatabaseMixin:
    def __init__(self):
        engine = create_engine(url=AIRTEXT_DATABASE_URL)
        self.database = sessionmaker(engine)
