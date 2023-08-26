from airtext.crud.contact import ContactAPI
from airtext.crud.group import GroupAPI
from airtext.crud.group_contact import GroupContactAPI
from airtext.crud.member import MemberAPI
from airtext.crud.message import MessageAPI


class Airtext:

    def __init__(self):
        self.contacts = ContactAPI()
        self.groups = GroupAPI()
        self.group_contacts = GroupContactAPI()
        self.members = MemberAPI()
        self.messages = MessageAPI()
