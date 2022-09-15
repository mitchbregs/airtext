from airtext.controllers.twilio_webhooks.parser import MessageParser


class MessageRequest:
    def __init__(self, event: dict):
        self.event = event

    def parse_message(self):
        parser = MessageParser(event=self.event)
        parsed = parser.parse()
        return parsed
