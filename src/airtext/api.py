from airtext.models.contact import AirtextContacts
from airtext.models.member import AirtextMembers
from airtext.models.message import AirtextMessages


class AirtextAPI:
    @property
    def contacts(self):
        return AirtextContacts()

    @property
    def members(self):
        return AirtextMembers()

    @property
    def messages(self):
        return AirtextMessages()
