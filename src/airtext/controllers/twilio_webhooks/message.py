import re
from dataclasses import dataclass
from typing import List, Tuple
from urllib.parse import unquote_plus

from airtext.api import AirtextAPI
from airtext.controllers.base import Controller, Request
from airtext.views.twilio_webhooks.message import Incoming, Outgoing


class MessageController(Controller):
    def __init__(self, request: Request):
        super().__init__(request=request)

    def dispatch_request(self):
        message = self.request.parse_message()
        member = self.api.members.get_by_proxy_number(proxy_number=message.to_number)

        if message.from_number == member.number:
            request = Outgoing(member=member, message=message)
        else:
            request = Incoming(member=member, message=message)

        request.send()
