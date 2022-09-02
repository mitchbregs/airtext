from airtext.api import AirtextAPI
from airtext.controllers.twilio_webhook import MessageParserData
from airtext.models.member import Member


class View:
    def __init__(self, member: Member, message: MessageParserData):
        self.member = member
        self.message = message
        self.api = AirtextAPI()
