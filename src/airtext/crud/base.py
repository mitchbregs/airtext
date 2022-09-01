from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from twilio.rest import Client

from airtext.config import MESSAGES_DATABASE_URL, TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN


class DatabaseMixin:
    def __init__(self):
        engine = create_engine(url=MESSAGES_DATABASE_URL)
        self.database = sessionmaker(engine)


class TwilioMixin:
    def __init__(self):
        self.twilio = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
