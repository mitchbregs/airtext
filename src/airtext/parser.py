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

    ERROR_MESSAGES = {
        "invalid-command": (
            "You either did not provide a command 🤔, or the command you "
            "provided is invalid. 🙅\n\n"
            "The accepted commands are as follows:\n"
            "❓ COMMANDS\n"
            "📲 TO\n"
            "📗 ADD\n"
            "🔎 GET\n"
            "🗑 DELETE\n"
            "📝 UPDATE\n"
        ),
        "number-not-found": (
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
        "body-not-found": (
            "We could not find any text or content to send. 🖇\n\n"
            "If you are sending a message to a contact, make sure to include a body of text or something!"
        ),
        "name-not-found": (
            "We could not find a name for your contact. 👤\n\n"
            "If you are trying to update a contact, make sure to include their name. "
            "For example, UPDATE +19876543210 @JaneDoe."
        )
    }

    def __init__(self, text: str):
        self.text = text
        self.error = False
        self.error_message = None
    
    def parse(self):
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
        pattern = re.compile(self.REGEX_COMMANDS["command"])
        search = pattern.search(self.text)

        if not search:
            self.error = True
            self.error_message = self.ERROR_MESSAGES["invalid-command"]
            return None

        command = search.group()
        
        if not command in self.COMMANDS:
            self.error = True
            self.error_message = self.ERROR_MESSAGES["invalid-command"]
            return None        

        return command

    def get_number(self):
        pattern = re.compile(self.REGEX_COMMANDS["number"])
        search = pattern.search(self.text)

        if not search:
            self.error = True
            self.error_message = self.ERROR_MESSAGES["number-not-found"]
            return None

        number = search.group()
        number = re.sub(r"[^\w]", "", number)

        if len(number) == 10:
            number = f"+1{number}"
        if len(number) == 11:
            number = f"+{number}"

        # TODO: We should make sure we are handling other cases...q
        
        return number

    def get_name(self):
        pattern = re.compile(self.REGEX_COMMANDS["name"])
        search = pattern.search(self.text)

        if not search:
            self.error_message = self.ERROR_MESSAGES["name-not-found"]
            return None

        name = search.group()

        return name
    

    def get_body(self):
        pattern = re.compile(self.REGEX_COMMANDS["body"])
        search = pattern.search(self.text)

        if not search:
            self.error_message = self.ERROR_MESSAGES["body-not-found"]
            return None
        
        body = search.group()

        return body
