from abc import ABC, abstractmethod
from urllib import parse

from airtext.parser import AirtextParser
from airtext.proxy import AirtextProxy

PREHOOK = "FROM @airtext\n\n"
POSTHOOK = ""
TEMPLATES = {
    "incoming": ("FROM {number} @{name}\n\n{text}"),
    "command-not-found": PREHOOK
    + (
        "You either did not provide a command 🤔, or the command you "
        "provided is invalid. 🙅\n\n"
        "The accepted commands are as follows:\n"
        "📲 TO\n"
        "📗 ADD\n"
        "🔎 GET\n"
        "🗑 DELETE\n"
        "📝 UPDATE\n"
    ),
    "number-not-found": PREHOOK
    + (
        "The phone number you provided either does not exist or "
        "is not properly formatted. 📵\n\n"
        "Examples of valid phone number formats:\n"
        "⚪️ +19876543210\n"
        "🔴 19876543210\n"
        "🟠 9876543210\n"
        "🟡 +1 (987) 654-3210\n"
        "🟢 1 (987) 654-3210\n"
        "🔵 (987) 654-3210\n"
        "🟣 987.654.3210\n"
        "⚫️ 1.987.654.3210\n"
    ),
    "name-not-found": PREHOOK
    + (
        "We could not find a name for your contact. 👤\n\n"
        "If you are trying to update a contact, make sure to include their @name.\n\n"
        "For example, UPDATE +19876543210 @JaneDoe."
    ),
    "body-not-found": PREHOOK
    + (
        "We could not find any text or content to send. 🖇\n\n"
        "If you are sending a message to a contact, make sure to include a body of text or something!"
    ),
    "add-contact": PREHOOK + ("🎉 Added new contact!\n\n{number} @{name}"),
    "add-contact-fail": PREHOOK + (
        "🤔 Hmmm, we could not add that contact for you. "
        "Are you sure it does not already exist?\n\n"
        "Try GET {number}."
    ),
    "get-contact": PREHOOK
    + ("Found the contact you were looking for! 😎\n\n{number} @{name}"),
    "get-contact-fail": PREHOOK
    + ("🥸 We were not able to find that contact for you. "
    "Have you tried adding it?\n\n"
    "Try ADD {number}."),
    "update-contact": PREHOOK + ("✍️ Updated contact.\n\n{number} @{name}"),
    "delete-contact": PREHOOK + ("👻 Deleted contact.\n\n{number} @{name}"),
    "delete-contact-fail": PREHOOK + (
        "Something went wrong trying to delete that contact. "
        "Perhaps you may have not had it in your contact list. 😵‍💫\n\n"
        "Try ADD {number}."
    ),
    "commands": PREHOOK
    + (
        "The accepted commands are as follows:\n"
        "📲 TO\n"
        "📗 ADD\n"
        "🔎 GET\n"
        "🗑 DELETE\n"
        "📝 UPDATE\n"
    ),
}


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

    @abstractmethod
    def handle(self):
        pass


class Incoming(TextMessage):
    def __init__(self, proxy: AirtextProxy):
        super().__init__(proxy=proxy)

    def handle(self):
        # Sending incoming message to proxy member
        self.proxy.send(
            to=self.proxy.member.number,
            body=TEMPLATES["incoming"].format(
                number=self.proxy.from_number,
                text=self.proxy.text,
                name=self.proxy.contact.name if self.proxy.contact else None,
            ),
        )

        # Add incoming message to database
        self.proxy.api.messages.add_message(
            proxy_number=self.proxy.proxy_number,
            from_number=self.proxy.from_number,
            member_id=self.proxy.member.id,
            command=None,
            number=None,
            name=None,
            body=self.proxy.text,
            error=False,
            error_message=None,
        )

        return


class Outgoing(TextMessage):
    def __init__(self, proxy: AirtextProxy):
        super().__init__(proxy=proxy)

    @property
    def parser(self):
        return AirtextParser(text=self.proxy.text)

    def handle(self):
        message_data = self.parser.parse()

        # Add outgoing message to database
        self.proxy.api.messages.add_message(
            proxy_number=self.proxy.proxy_number,
            from_number=self.proxy.from_number,
            member_id=self.proxy.member.id,
            command=message_data.command,
            number=message_data.number,
            name=message_data.name,
            body=message_data.body,
            error=message_data.error,
            error_message=message_data.error_message,
        )

        # Message handling
        if message_data.error:
            self.proxy.send(
                to=self.proxy.member.number,
                body=TEMPLATES[message_data.error_message],
            )

            return

        # Return list of possible actions
        if message_data.command == "COMMANDS":
            self.proxy.send(
                to=self.proxy.member.number,
                body=TEMPLATES["commands"],
            )

            return

        # Add a new contact
        if message_data.command == "ADD":

            is_added = self.proxy.api.contacts.add_contact(
                name=message_data.name,
                number=message_data.number,
                member_id=self.proxy.member.id,
            )

            # Success
            if is_added:
                self.proxy.send(
                    to=self.proxy.member.number,
                    body=TEMPLATES["add-contact"].format(
                        number=message_data.number,
                        name=message_data.name,
                    ),
                )

                return

            # Fail
            self.proxy.send(
                to=self.proxy.member.number,
                body=TEMPLATES["add-contact-fail"].format(
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
                    body=TEMPLATES["get-contact"].format(
                        number=contact.number,
                        name=contact.name,
                    ),
                )

                return

            # Contact does not exist, respond error and return
            self.proxy.send(
                to=self.proxy.member.number,
                body=TEMPLATES["get-contact-fail"].format(
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
                    body=TEMPLATES["update-contact"].format(
                        number=message_data.number,
                        name=message_data.name,
                    ),
                )

                return

            # Contact does not exist, respond error and return
            self.proxy.send(
                to=self.proxy.member.number,
                body=TEMPLATES[message_data.error_message].format(
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
                    body=TEMPLATES["delete-contact"].format(
                        number=message_data.number,
                        name=message_data.name,
                    ),
                )

                return

            # Contact does not exist, respond error and return
            self.proxy.send(
                to=self.proxy.member.number,
                body=TEMPLATES["delete-contact-fail"].format(
                    number=message_data.number,
                    name=message_data.name,
                ),
            )

            return

        if message_data.command == "TO":

            # Send message
            self.proxy.send(
                to=message_data.number,
                body=message_data.body,
            )

            return
