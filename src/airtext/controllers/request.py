from typing import List
from urllib import parse

from airtext.controllers.parser import TextParser


class MessageRequest:
    def __init__(self, event):
        self.event = event
        self.query_string = self.event["body"]
        self.query_params = parse.parse_qs(qs=self.query_string)

        self.to_number = self.query_params["To"][0]
        self.from_number = self.query_params["From"][0]
        self.text = self.query_params["Body"][0]

    def __repr__(self):
        return (
            f"<MessageEvent to_number={self.to_number} from_number={self.from_number}>"
        )

    def parse_text(self, is_incoming: bool = False):
        parser = TextParser(text=self.text)
        text = parser.parse(is_incoming=is_incoming)
        return text
