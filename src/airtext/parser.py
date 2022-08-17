"""Parsing text messages.

Examples
--------

- COMMANDS

- ADD 1XXXXXXXXXX
- ADD 1XZXZXZXZXZ,1XXXXXXXXXX
- ADD 1XXXXXXXXXX @Mitch
- ADD 1XXXXXXXXXX @Mitch,1XZXZXZXZXZ 
- GET 1XXXXXXXXXX
- GET all
- DELETE 1XXXXXXXXXX
- DELETE 1XXXXXXXXXX,1XZXZXZXZXZ
- DELETE all
- UPDATE 1XZXZXZXZXZ @Chuck
- UPDATE 1XXXXXXXXXX @Chuck, 1XZXZXZXZXZ @Mitch
- TO 1XXXXXXXXXX
  yooo
- TO 1XXXXXXXXXX,1XZXZXZXZXZ
  yooooooo
- TO all
  yooooooo

EVENTUALLY
- ADD @Mitch #CentralNJ
- ADD 1XXXXXXXXXX #CentralNJ

-------
PICK OUT: Command [ADD, GET, DELETE, UPDATE, TO, COMMANDS]
          Phone number (1XZXZXZXZXZ) - can come in formats: +192039402, 1 234234234, 1 (234) 324- 2342 --> eventually becomes +1XXXXXXXXXX
          Name (@Mitch) ----> eventually becomes Mitch
          Campaign (#CentralNJ) -----> becomes CentralNJ
          Body.... : yooo when exists a TO command
"""
import re
from dataclasses import dataclass


@dataclass
class AirtextParserData:
    command: str
    number: str
    name: str
    body: str
    error: bool
    error_message: str


class AirtextParserError:
    COMMAND_NOT_FOUND: str = "command-not-found"
    NUMBER_NOT_FOUND: str = "number-not-found"
    NAME_NOT_FOUND: str = "name-not-found"
    BODY_NOT_FOUND: str = "body-not-found"


class AirtextParser:

    COMMANDS = {
        "COMMANDS",
        "ADD",
        "GET",
        "DELETE",
        "UPDATE",
        "TO",
    }

    REGEX_COMMANDS = {
        "command": r"^(ADD|GET|DELETE|UPDATE|TO|COMMANDS)",
        "number": r"(\+\d{1,2}\s?)?1?\-?\.?\s?\(?\d{3}\)?[\s.-]?\d{3}[\s.-]?\d{4}",
        "name": r"(?<=@)(.*?)(?=\,|$|\s+|\:|\;)",
        "body": r"(?<=\n)(.*)$",
    }

    def __init__(self, text: str):
        self.text = text
        self.error = False
        self.error_message = None

    def parse(self):

        # Reverse order of significance
        body = self.get_body()
        name = self.get_name()
        number = self.get_number()
        command = self.get_command()

        return AirtextParserData(
            command=command,
            number=number,
            name=name,
            body=body,
            error=self.error,
            error_message=self.error_message,
        )

    def get_command(self):
        """Search for the command."""
        # TODO: Make case insensitive
        pattern = re.compile(self.REGEX_COMMANDS["command"])
        search = pattern.search(self.text)

        if not search:
            self.error = True
            self.error_message = AirtextParserError.COMMAND_NOT_FOUND
            return None

        command = search.group()

        return command

    def get_number(self):
        """Search for number.

        - If not exists, return error code.
        - If exists, remove all symbols
        -- If length checks, format for insert and insert.
        """
        pattern = re.compile(self.REGEX_COMMANDS["number"])
        search = pattern.search(self.text)

        if not search:
            self.error = True
            self.error_message = AirtextParserError.NUMBER_NOT_FOUND
            return None

        number = search.group()
        number = re.sub(r"[^\w]", "", number)

        if len(number) == 10:
            number = f"+1{number}"
        elif len(number) == 11:
            number = f"+{number}"
        else:
            self.error = True
            self.error_message = AirtextParserError.NUMBER_NOT_FOUND
            return

        # TODO: We should make sure we are handling other cases...

        return number

    def get_name(self):
        pattern = re.compile(self.REGEX_COMMANDS["name"])
        search = pattern.search(self.text)

        if not search:
            self.error_message = AirtextParserError.NAME_NOT_FOUND
            return None

        name = search.group()

        return name

    def get_body(self):
        pattern = re.compile(self.REGEX_COMMANDS["body"])
        search = pattern.search(self.text)

        if not search:
            self.error_message = AirtextParserError.BODY_NOT_FOUND
            return None

        body = search.group()

        return body
