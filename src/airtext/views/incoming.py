from airtext.controllers.parser import MessageParserData
from airtext.models.member import Member
from airtext.views.base import View
from airtext.views.response import IncomingResponse


class Incoming(View):
    """Handles incoming message end-user result."""

    def __init__(self, member: Member, message: MessageParserData):
        super().__init__(member=member, message=message)

    def send(self):
        """Sends a message and stores record."""
        contact = self.api.contacts.get_by_number_and_member_id(
            number=self.message.from_number, member_id=self.member.id
        )
        name = contact.name if contact else None

        self.api.messages.create(
            from_number=self.message.from_number,
            to_number=self.message.to_number,
            body_content=self.message.body_content,
            media_content=self.message.media_content,
            proxy_number=self.member.proxy_number,
            member_id=self.member.id,
            command=None,
            numbers=[
                self.member.number,
            ],
            names=[],
            groups=[],
            body=IncomingResponse.ALL.format(
                number=self.message.from_number,
                name=name,
                body_content=self.message.body_content,
            ),
            error=False,
            error_code=None,
        )
