from airtext.models.contact import AirtextContacts
from airtext.models.member import AirtextMembers


class AirtextAPI:
    def __init__(self):
        self.contacts = AirtextContacts()
        self.members = AirtextMembers()
