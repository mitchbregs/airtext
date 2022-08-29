from airtext.api import AirtextAPI
from airtext.controllers.base import Controller
from airtext.controllers.request import MessageRequest
from airtext.views.incoming import Incoming
from airtext.views.outgoing import Outgoing


class MessageController(Controller):
    def __init__(self, request: MessageRequest):
        super().__init__(request=request)
        self.api = AirtextAPI()

    def dispatch_request(self):
        member = self.api.members.get_by_proxy_number(
            proxy_number=self.request.to_number
        )

        if self.request.from_number == member.number:
            text = self.request.parse_text(is_incoming=False)
            message = Outgoing(member=member, text=text)
        else:
            text = self.request.parse_text(is_incoming=True)
            message = Incoming(
                member=member, from_number=self.request.from_number, text=text
            )

        message.send()
