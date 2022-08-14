"""Parsing text messages.

Examples
--------
HELP
ADD 1XXXXXXXXXX
ADD 1XZXZXZXZXZ,1XXXXXXXXXX
ADD 1XXXXXXXXXX Mitch
ADD 1XXXXXXXXXX Mitch,1XZXZXZXZXZ 
GET 1XXXXXXXXXX
GET all
DELETE 1XXXXXXXXXX
DELETE 1XXXXXXXXXX,1XZXZXZXZXZ
DELETE all
UPDATE 1XZXZXZXZXZ Chuck
UPDATE 1XXXXXXXXXX Chuck, 1XZXZXZXZXZ Mitch
TO 1XXXXXXXXXX
TO 1XXXXXXXXXX,1XZXZXZXZXZ
TO all
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


class AirtextParser:

    COMMANDS = {
        "COMMANDS",
        "ADD",
        "GET",
        "DELETE",
        "UPDATE",
        "TO",
    }

    ERROR_MESSAGES = {
        "command-not-found": "The command you provided does not exist.",
        "phone-not-found": "The phone you provided is not properly formatted.",
    }

    def __init__(self, text: str):
        self.text = text
    
    def parse(self):
        command = self.get_command()
        number = self.get_number()
        name = self.get_name()
        body = self.get_body()
        error = self.error
        error_message = self.error_message

        return AirtextParserData(
            command=command,
            number=number,
            name=name,
            body=body,
            error=error,
            error_message=error_message,
        )
    
    @property
    def arguments(self):
        try:
            return self.text.strip().split(" ", 1)[1].strip().upper()
        except IndexError:
            return []

    def get_command(self):
        command = self.text.strip().split(" ", 1)[0].strip().upper()
        
        if not command in self.COMMANDS:
            self.error = True
            self.error_message = self.ERROR_MESSAGES["command-not-found"]
            return None        

        return command

    def get_number(self):
        return None
        # wo_symbols = re.sub(r"[^\w]", " ", self.arguments.splt)

        # try:
        #     search_number = wo_symbols # DO SOMETHING
        # except Exception:
        #     return 
        # number = f"+1{search_number}"
        # return number

    def get_name(self):
        if len(self.arguments) > 1:
            return self.arguments.split(" ")[1].strip()
        else:
            return None

    def get_body(self):
        return self.text.split("\n", 1)[-1]