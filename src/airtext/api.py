from airtext.models.contact import ContactAPI
from airtext.models.member import MemberAPI
from airtext.models.message import MessageAPI


class AirtextAPI:
    @property
    def contacts(self):
        return ContactAPI()

    @property
    def members(self):
        return MemberAPI()

    @property
    def messages(self):
        return MessageAPI()
