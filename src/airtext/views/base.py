from airtext.api import AirtextAPI
from airtext.controllers.base import RequestParserData
from airtext.models.member import Member


class View:
    def __init__(self, member: Member, message: RequestParserData):
        self.member = member
        self.message = message
        self.api = AirtextAPI()
