from typing import List

from airtext.controllers.parser import MessageParser


class MessageRequest:
    def __init__(self, event: dict):
        self.event = event

    def parse_message(self):
        parser = MessageParser(event=self.event)
        message = parser.parse()
        return message
