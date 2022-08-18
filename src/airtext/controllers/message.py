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
        text = self.api.messages.parse_text(text=self.request.text)

        if self.request.from_number == member.number:
            message = Outgoing(member=member, text=text)
        else:
            message = Incoming(
                member=member, from_number=request.from_number, text=text
            )

        message.send()
