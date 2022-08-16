from abc import ABC, abstractmethod
from urllib import parse

from airtext.parser import AirtextParser
from airtext.proxy import AirtextProxy


class MessageEvent:
    def __init__(self, event):
        self.event = event
        self.query_string = self.event["body"]
        self.query_params = parse.parse_qs(qs=self.query_string)

        self.to_number = self.query_params["To"][0]
        self.from_number = self.query_params["From"][0]
        self.text = self.query_params["Body"][0]

    def __repr__(self):
        return f"<MessageEvent to_number={self.to_number} from_number={self.from_number}>"

    def get_airtext_proxy(self):
        return AirtextProxy(
            proxy_number=self.to_number,
            from_number=self.from_number,
            text=self.text,
        )


class Message(ABC):

    def __init__(self, proxy: AirtextProxy):
        self.proxy = proxy

    @abstractmethod
    def handle(self):
        pass


class Incoming(Message):

    INCOMING_MESSAGE_TEMPLATE = "FROM {number}\n\n{text}"

    def __init__(self, proxy: AirtextProxy):
        super().__init__(proxy=proxy)

    def handle(self):
        self.proxy.send_message(
            to=self.proxy.member.number,
            body=self.INCOMING_MESSAGE_TEMPLATE.format(
                number=self.proxy.from_number,
                text=self.proxy.text
            )
        )

        return


class Outgoing(Message):

    PRE = "FROM mitch@airtext.io\n\n\n"
    ERROR_TEMPLATE = PRE + "{text}\n\nText COMMANDS to learn more."
    COMMANDS_TEMPLATE = PRE + "This will eventually be a rule book..."
    ADD_CONTACT_TEMPLATE = PRE + "Successfully added new contact:\n\n{number} @{name}"
    DELETE_CONTACT_TEMPLATE = PRE + "Deleted contact:\n\n{number}"

    def __init__(self, proxy: AirtextProxy):
        super().__init__(proxy=proxy)

    @property
    def parser(self):
        return AirtextParser(text=self.proxy.text)

    def handle(self):
        message_data = self.parser.parse()

        if message_data.command == "COMMANDS":
            self.proxy.send_message(
                to=self.proxy.member.number,
                body=self.COMMANDS_TEMPLATE,
            )

            return

        if message_data.error:
            self.proxy.send_message(
                to=self.proxy.member.number,
                body=self.ERROR_TEMPLATE.format(
                    text=message_data.error_message,
                )
            )

            return

        if message_data.command == "ADD":
            self.proxy.api.contacts.add_contact(
                name=message_data.name,
                number=message_data.number,
                member_id=self.proxy.member.id,
            )      

            self.proxy.send_message(
                to=self.proxy.member.number,
                body=self.ADD_CONTACT_TEMPLATE.format(
                    number=message_data.number,
                    name=message_data.name,
                )
            )

            return

        if message_data.command == "GET":
            # TODO
            self.proxy.send_message(
                to=self.proxy.member.number,
                body="Under construction!!"
            )

            return

        if message_data.command == "DELETE":
            self.proxy.api.contacts.delete_contact(
                number=message_data.number,
                member_id=self.proxy.member.id,
            )

            self.proxy.send_message(
                to=self.proxy.member.number,
                body=self.DELETE_CONTACT_TEMPLATE.format(
                    number=number,
                )
            )

            return

        if message_data.command == "UPDATE":
            self.proxy.api.contacts.update_contact(
                number=message_data.number,
                name=message_data.name,
                member_id=self.proxy.member.id,
            )

            return

        if message_data.command == "TO":
            self.proxy.send_message(
                to=message_data.number,
                body=message_data.body,

            )

            return


