from airtext.api import AirtextAPI
from airtext.models.member import Member
from airtext.views.base import View
from airtext.views.response import IncomingResponse


class Incoming(View):
    """Handles incoming message end-user result."""

    def __init__(self, member: Member, from_number: str, text: str):
        self.member = member
        self.from_number = from_number
        self.text = text
        self.api = AirtextAPI()

    def send(self):
        """Sends a message and stores record."""
        contact = self.api.contacts.get_by_number_and_member_id(
            number=self.from_number, member_id=self.member.id
        )
        name = contact.name if contact else None

        self.api.messages.create(
            proxy_number=member.proxy_number,
            from_number=self.from_number,
            member_id=member.id,
            command=None,
            number=None,
            body=IncomingResponse.format(number=self.from_number, name=name),
            error=None,
            error_message=None,
        )
