from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from twilio.rest import Client

from airtext.config import MESSAGES_DATABASE_URL, TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN

Base = declarative_base()
metadata = Base.metadata


class ExternalConnectionsMixin:
    def __init__(self):
        engine = create_engine(url=MESSAGES_DATABASE_URL)
        self.database = sessionmaker(engine)
        self.twilio = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
