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
        return (
            f"<MessageEvent to_number={self.to_number} from_number={self.from_number}>"
        )

    def get_airtext_proxy(self):
        return AirtextProxy(
            proxy_number=self.to_number,
            from_number=self.from_number,
            text=self.text,
        )


class TextMessage(ABC):
    def __init__(self, proxy: AirtextProxy):
        self.proxy = proxy

    def add_message(
        self,
        command: str,
        number: str,
        name: str,
        body: str,
        error: bool,
        error_message: str,
    ):
        self.proxy.api.messages.add_message(
            from_number=self.proxy.from_number,
            proxy_number=self.proxy.proxy_number,
            member_id=self.proxy.member.id,
            command=command,
            number=number,
            name=name,
            body=body,
            error=error,
            error_message=error_message,
        )

        return

    @abstractmethod
    def handle(self):
        pass


class Incoming(TextMessage):

    INCOMING_MESSAGE_TEMPLATE = "FROM {number} @{name}\n\n{text}"

    def __init__(self, proxy: AirtextProxy):
        super().__init__(proxy=proxy)

    def handle(self):
        # Sending incoming message to proxy member
        self.proxy.send(
            to=self.proxy.member.number,
            body=self.INCOMING_MESSAGE_TEMPLATE.format(
                number=self.proxy.from_number,
                text=self.proxy.text,
                name=self.proxy.contact.name if self.proxy.contact else None,
            ),
        )

        # Add incoming message to database
        self.add_message(
            command=None,
            number=None,
            name=None,
            body=self.proxy.text,
            error=False,
            error_message=None,
        )

        return


class Outgoing(TextMessage):

    PRE = "FROM mitch@airtext.io\n\n"
    ERROR_TEMPLATE = PRE + "{text}\n\nText COMMANDS to learn more."
    COMMANDS_TEMPLATE = PRE + "This will eventually be a rule book..."
    ADD_CONTACT_TEMPLATE = PRE + "Successfully added new contact!\n\n{number} @{name}"
    GET_CONTACT_TEMPLATE = PRE + "Looks like we found a contact!\n\n{number} @{name}"
    DELETE_CONTACT_TEMPLATE = PRE + "Deleted contact:\n\n{number} @{name}"
    UPDATE_CONTACT_TEMPLATE = PRE + "Updated contact:\n\n{number} @{name}"

    NOT_FOUND_CONTACT = PRE + "Could not find contact.\n\n{number} @{name}"

    def __init__(self, proxy: AirtextProxy):
        super().__init__(proxy=proxy)

    @property
    def parser(self):
        return AirtextParser(text=self.proxy.text)

    def handle(self):
        message_data = self.parser.parse()

        # Message handling
        if message_data.command == "COMMANDS":
            self.proxy.send(
                to=self.proxy.member.number,
                body=self.COMMANDS_TEMPLATE,
            )

        if message_data.error:
            self.proxy.send(
                to=self.proxy.member.number,
                body=self.ERROR_TEMPLATE.format(
                    text=message_data.error_message,
                ),
            )

        if message_data.command == "ADD":

            self.proxy.api.contacts.add_contact(
                name=message_data.name,
                number=message_data.number,
                member_id=self.proxy.member.id,
            )

            self.proxy.send(
                to=self.proxy.member.number,
                body=self.ADD_CONTACT_TEMPLATE.format(
                    number=message_data.number,
                    name=message_data.name,
                ),
            )

            return

        if message_data.command == "GET":

            # Search on number or name
            if message_data.number:
                contact = self.proxy.api.contacts.get_by_number_and_member_id(
                    number=message_data.number,
                    member_id=self.proxy.member.id,
                )
            elif message_data.name:
                contact = self.proxy.api.contacts.get_by_name_and_member_id(
                    name=message_data.name,
                    member_id=self.proxy.member.id,
                )

            # If contact exsists, repond success and return
            if contact:
                self.proxy.send(
                    to=self.proxy.member.number,
                    body=self.GET_CONTACT_TEMPLATE.format(
                        number=contact.number,
                        name=contact.name,
                    ),
                )

                return

            # Contact does not exist, respond error and return
            self.proxy.send(
                to=self.proxy.member.number,
                body=self.NOT_FOUND_CONTACT.format(
                    number=message_data.number,
                    name=message_data.name,
                ),
            )

            return

        if message_data.command == "DELETE":

            # Try to delete contact based on number
            is_deleted = self.proxy.api.contacts.delete_contact(
                number=message_data.number,
                member_id=self.proxy.member.id,
            )

            # If deleted, respond success and return
            if is_deleted:
                self.proxy.send(
                    to=self.proxy.member.number,
                    body=self.DELETE_CONTACT_TEMPLATE.format(
                        number=message_data.number,
                        name=message_data.name,
                    ),
                )

                return

            # Contact does not exist, respond error and return
            self.proxy.send(
                to=self.proxy.member.number,
                body=self.NOT_FOUND_CONTACT.format(
                    number=message_data.number,
                    name=message_data.name,
                ),
            )

            return

        if message_data.command == "UPDATE":

            # Try to update the contact
            is_updated = self.proxy.api.contacts.update_contact(
                number=message_data.number,
                name=message_data.name,
                member_id=self.proxy.member.id,
            )

            # If updated, respond success and return
            if is_updated:
                self.proxy.send(
                    to=self.proxy.member.number,
                    body=self.UPDATE_CONTACT_TEMPLATE.format(
                        number=message_data.number,
                        name=message_data.name,
                    ),
                )

                return

            # Contact does not exist, respond error and return
            self.proxy.send(
                to=self.proxy.member.number,
                body=self.NOT_FOUND_CONTACT.format(
                    number=message_data.number,
                    name=message_data.name,
                ),
            )

            return

        if message_data.command == "TO":
            self.proxy.send(
                to=message_data.number,
                body=message_data.body,
            )

            return

        # Add outgoing message to database
        self.add_message(
            command=message_data.command,
            number=message_data.number,
            name=message_data.name,
            body=message_data.body,
            error=message_data.error,
            error_message=message_data.error_message,
        )
