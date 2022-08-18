import re
from dataclasses import dataclass

from airtext.models.base import Message
from airtext.models.mixin import ExternalConnectionsMixin


class MessageAPI(ExternalConnectionsMixin):
    def create(
        self,
        proxy_number: str,
        to_number: str,
        member_id: int,
        command: str,
        number: str,
        name: str,
        body: str,
        error: bool,
        error_code: bool,
    ):
        with self.database() as session:
            message = Message(
                proxy_number=proxy_number,
                to_number=to_number,
                member_id=member_id,
                command=command,
                number=number,
                name=name,
                body=body,
                error=error,
                error_code=error_code,
            )
            session.add(message)
            session.commit()

        self.twilio.messages.create(
            to=to_number,
            from_=proxy_number,
            body=body,
        )

        return True

    def parse_text(self, text: str, is_incoming: bool = False):
        parser = TextParser(text=text)
        text = parser.parse(is_incoming=is_incoming)
        return text


class TextRegex:
    COMMAND = r"^(ADD|GET|DELETE|UPDATE|TO|AIRTEXT)"
    NUMBER = r"(\+\d{1,2}\s?)?1?\-?\.?\s?\(?\d{3}\)?[\s.-]?\d{3}[\s.-]?\d{4}"
    NAME = r"(?<=@)(.*?)(?=\,|$|\s+|\:|\;)"
    BODY = r"\n(.*)?"


class TextCommand:
    AIRTEXT: str = "AIRTEXT"
    TO: str = "TO"
    ADD: str = "ADD"
    GET: str = "GET"
    UPDATE: str = "UPDATE"
    DELETE: str = "DELETE"


class TextError:
    COMMAND_NOT_FOUND: str = "command-not-found"
    NUMBER_NOT_FOUND: str = "number-not-found"
    NAME_NOT_FOUND: str = "name-not-found"
    BODY_NOT_FOUND: str = "body-not-found"


@dataclass
class TextParserData:
    command: str
    number: str
    name: str
    body: str
    error: bool
    error_code: str


class TextParser:
    def __init__(self, text: str):
        self.text = text

    def parse(self, is_incoming: bool):
        command = self.get_command()
        number = self.get_number()
        name = self.get_name()
        body = self.get_incoming_body() if is_incoming else self.get_outgoing_body()
        error = False
        error_code = None

        if command == TextCommand.AIRTEXT:
            error = False
            error_code = None
            body = ""
        elif command == TextCommand.TO:
            if not any([number, name]):
                error = True
                error_code = TextError.NUMBER_NOT_FOUND
            if not body:
                error = True
                error_code = TextError.BODY_NOT_FOUND
        elif command == TextCommand.ADD:
            if not any([number, name]):
                error = True
                error_code = TextError.NUMBER_NOT_FOUND
        elif command == TextCommand.GET:
            if not any([number, name]):
                error = True
                error_code = TextError.NUMBER_NOT_FOUND
        elif command == TextCommand.UPDATE:
            if not number:
                error = True
                error_code = TextError.NUMBER_NOT_FOUND
            if not name:
                error = True
                error_code = TextError.NAME_NOT_FOUND
        elif command == TextCommand.DELETE:
            if not any([number, name]):
                error = True
                error_code = TextError.NUMBER_NOT_FOUND
        else:
            error = True
            error_code = TextError.COMMAND_NOT_FOUND

        return TextParserData(
            command=command,
            number=number,
            name=name,
            body=body,
            error=error,
            error_code=error_code,
        )

    def get_command(self):
        """Search for the command."""
        pattern = re.compile(TextRegex.COMMAND, re.IGNORECASE)
        search = pattern.search(self.text)

        command = search.group() if search else None

        return command

    def get_number(self):
        """Search for number.

        - If not exists, return error code.
        - If exists, remove all symbols
        -- If length checks, format for insert and insert.
        """
        pattern = re.compile(TextRegex.NUMBER)
        search = pattern.search(self.text)

        if not search:
            return None

        number = search.group()
        number = re.sub(r"[^\w]", "", number)

        if len(number) == 10:
            number = f"+1{number}"
        elif len(number) == 11:
            number = f"+{number}"
        else:
            number = None

        return number

    def get_name(self):
        pattern = re.compile(TextRegex.NAME)
        search = pattern.search(self.text)

        name = search.group() if search else None

        return name

    def get_incoming_body(self):
        return self.text

    def get_outgoing_body(self):
        pattern = re.compile(TextRegex.BODY, flags=re.DOTALL)
        search = pattern.search(self.text)

        body = search.group().strip() if search else None

        return body
