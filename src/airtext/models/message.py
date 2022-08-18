import re
from dataclasses import dataclass

from sqlalchemy import Column, ForeignKey, UniqueConstraint, text
from sqlalchemy.dialects.postgresql import BOOLEAN, INTEGER, TIMESTAMP, VARCHAR

from airtext.models.mixin import ExternalConnectionsMixin, Base


class Message(Base):

    __tablename__ = "messages"

    id = Column(INTEGER, primary_key=True)
    proxy_number = Column(VARCHAR(12), nullable=False)
    to_number = Column(VARCHAR(12))
    member_id = Column(INTEGER, ForeignKey("members.id"))
    command = Column(VARCHAR(12))
    number = Column(VARCHAR(12))
    name = Column(VARCHAR(36))
    body = Column(VARCHAR(720))
    error = Column(BOOLEAN)
    error_code = Column(VARCHAR(720))
    created_on = Column(
        TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP")
    )


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


@dataclass
class TextParserData:
    command: str
    number: str
    name: str
    body: str
    error: bool
    error_code: str


class TextParserError:
    COMMAND_NOT_FOUND: str = "command-not-found"
    NUMBER_NOT_FOUND: str = "number-not-found"
    NAME_NOT_FOUND: str = "name-not-found"
    BODY_NOT_FOUND: str = "body-not-found"


class TextRegexCommands:
    COMMAND = r"^(ADD|GET|DELETE|UPDATE|TO|COMMANDS)"
    NUMBER = r"(\+\d{1,2}\s?)?1?\-?\.?\s?\(?\d{3}\)?[\s.-]?\d{3}[\s.-]?\d{4}"
    NAME = r"(?<=@)(.*?)(?=\,|$|\s+|\:|\;)"
    # GROUP = r"(?<=#)(.*?)(?=\,|$|\s+|\:|\;)"
    BODY = r"(?<=\n)(.*)"


class TextParser:
    def __init__(self, text: str):
        self.text = text
        self.error = False
        self.error_code = None

    def parse(self, is_incoming: bool):
        command = self.get_command()
        number = self.get_number()
        name = self.get_name()
        if is_incoming:
            body = self.get_incoming_body()
        else:
            body = self.get_outgoing_body()

        return TextParserData(
            command=command,
            number=number,
            name=name,
            body=body,
            error=self.error,
            error_code=self.error_code,
        )

    def get_command(self):
        """Search for the command."""
        pattern = re.compile(TextRegexCommands.COMMAND, re.IGNORECASE)
        search = pattern.search(self.text)

        if not search:
            self.error = True
            self.error_code = TextParserError.COMMAND_NOT_FOUND
            return None

        command = search.group()

        return command

    def get_number(self):
        """Search for number.

        - If not exists, return error code.
        - If exists, remove all symbols
        -- If length checks, format for insert and insert.
        """
        pattern = re.compile(TextRegexCommands.NUMBER)
        search = pattern.search(self.text)

        if not search:
            self.error = True
            self.error_code = TextParserError.NUMBER_NOT_FOUND
            return None

        number = search.group()
        number = re.sub(r"[^\w]", "", number)

        if len(number) == 10:
            number = f"+1{number}"
        elif len(number) == 11:
            number = f"+{number}"
        else:
            self.error = True
            self.error_code = TextParserError.NUMBER_NOT_FOUND
            return

        # TODO: We should make sure we are handling other cases...

        return number

    def get_name(self):
        pattern = re.compile(TextRegexCommands.NAME)
        search = pattern.search(self.text)

        if not search:
            self.error_code = TextParserError.NAME_NOT_FOUND
            return None

        name = search.group()

        return name

    def get_incoming_body(self):
        self.error = False
        self.error_code = None
        return self.text

    def get_outgoing_body(self):
        pattern = re.compile(TextRegexCommands.BODY)
        search = pattern.search(self.text)

        if not search:
            self.error_code = TextParserError.BODY_NOT_FOUND
            return None

        body = search.group()

        return body
