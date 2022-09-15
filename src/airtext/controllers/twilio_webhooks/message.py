import re
from dataclasses import dataclass
from typing import List, Tuple
from urllib.parse import unquote_plus

from airtext.api import AirtextAPI
from airtext.controllers.base import Controller
from airtext.controllers.twilio_webhooks.request import MessageRequest
from airtext.views.twilio_webhooks.message import Incoming, Outgoing


class MessageController(Controller):
    def __init__(self, message: MessageRequest):
        super().__init__(request=message)

    def dispatch_request(self):
        message = self.request.parse_message()
        member = self.api.members.get_by_proxy_number(proxy_number=message.to_number)

        if message.from_number == member.number:
            view = Outgoing(member=member, message=message)
        else:
            view = Incoming(member=member, message=message)

        view.send()
