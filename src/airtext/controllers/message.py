from airtext.api import AirtextAPI
from airtext.controllers.base import Controller
from airtext.controllers.request import MessageRequest
from airtext.views.incoming import Incoming
from airtext.views.outgoing import Outgoing


class MessageController(Controller):
    def __init__(self, request: MessageRequest):
        super().__init__(request=request)

    def dispatch_request(self):
        message = self.request.parse_message()
        member = self.api.members.get_by_proxy_number(
            proxy_number=message.to_number
        )

        if message.from_number == member.number:
            request = Outgoing(member=member, message=message)
        else:
            request = Incoming(member=member, message=message)

        request.send()
