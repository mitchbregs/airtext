from airtext.api import AirtextAPI
from airtext.controllers.base import RequestData
from airtext.models.member import Member


class View:
    def __init__(self, member: Member, request: RequestData):
        self.member = member
        self.request = request
        self.api = AirtextAPI()
