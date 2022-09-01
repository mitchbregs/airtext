from airtext.crud.contact import ContactAPI
from airtext.crud.group import GroupAPI
from airtext.crud.group_contact import GroupContactAPI
from airtext.crud.member import MemberAPI
from airtext.crud.message import MessageAPI


class AirtextAPI:
    @property
    def contacts(self):
        return ContactAPI()

    @property
    def group_contacts(self):
        return GroupContactAPI()

    @property
    def groups(self):
        return GroupAPI()

    @property
    def members(self):
        return MemberAPI()

    @property
    def messages(self):
        return MessageAPI()
