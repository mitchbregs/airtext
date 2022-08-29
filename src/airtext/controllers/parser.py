import re
from dataclasses import dataclass
from typing import List, Tuple


class TextRegex:
    COMMAND = r"^(AIRTEXT|TO|ADD|GET|UPDATE|DELETE|CREATE|PUT|REMOVE)"
    NUMBER = r"(\+\d{1,2}\s?)?1?\-?\.?\s?\(?\d{3}\)?[\s.-]?\d{3}[\s.-]?\d{4}"
    NAME = r"(?<=@)(.*?)(?=\,|$|\s+|\:|\;)"
    NUMBER_NAME = r"(\+\d{1,2}\s?)?1?\-?\.?\s?\(?\d{3}\)?[\s.-]?\d{3}[\s.-]?\d{4}\s+(?=@)(.*?)(?=\,|$|\s+|\:|\;)"
    GROUP = r"(?<=#)(.*?)(?=\,|$|\s+|\:|\;)"
    BODY = r"\n(.*)?"


class TextCommand:
    AIRTEXT: str = "AIRTEXT"
    TO: str = "TO"
    ADD: str = "ADD"
    GET: str = "GET"
    UPDATE: str = "UPDATE"
    DELETE: str = "DELETE"
    PUT: str = "PUT"
    REMOVE: str = "REMOVE"


class TextError:
    COMMAND_NOT_FOUND: str = "command-not-found"
    NUMBER_NOT_FOUND: str = "number-not-found"
    NAME_NOT_FOUND: str = "name-not-found"
    NUMBER_NAME_NOT_FOUND: str = "number-name-not-found"
    GROUP_NOT_FOUND: str = "group-not-found"
    BODY_NOT_FOUND: str = "body-not-found"


@dataclass
class TextParserData:
    command: str
    numbers: List[str]
    names: List[str]
    number_names: List[Tuple]
    groups: List[str]
    body: str
    error: bool
    error_code: str


class TextParser:
    def __init__(self, text: str):
        self.text = text

    def parse(self, is_incoming: bool):
        command = self.get_command()
        numbers = self.get_numbers()
        names = self.get_names()
        number_names = self.get_number_names()
        groups = self.get_groups()
        body = self.get_incoming_body() if is_incoming else self.get_outgoing_body()
        error = False
        error_code = None

        if command == TextCommand.AIRTEXT:
            error = False
            error_code = None
        elif command == TextCommand.TO:
            if not any([numbers, names, groups]):
                error = True
                error_code = TextError.NUMBER_NOT_FOUND
            elif not body:
                error = True
                error_code = TextError.BODY_NOT_FOUND
        elif command == TextCommand.ADD:
            if not any([numbers, names, number_names, groups]):
                error = True
                error_code = TextError.NUMBER_NOT_FOUND
        elif command == TextCommand.GET:
            if not any([numbers, names, groups]):
                error = True
                error_code = TextError.GROUP_NOT_FOUND
        elif command == TextCommand.UPDATE:
            if not numer_names:
                error = True
                error_code = TextError.NUMBER_NAME_NOT_FOUND
        elif command == TextCommand.DELETE:
            if not any([numbers, names, groups]):
                error = True
                error_code = TextError.NUMBER_NOT_FOUND
        elif command == TextCommand.PUT:
            if not any([numbers, names]):
                error = True
                error_code = TextError.NUMBER_NOT_FOUND
            if not groups:
                error = True
                error_code = TextError.GROUP_NOT_FOUND
        elif command == TextCommand.REMOVE:
            if not any([numbers, names]):
                error = True
                error_code = TextError.NUMBER_NOT_FOUND
            if not groups:
                error = True
                error_code = TextError.GROUP_NOT_FOUND
        else:
            error = True
            error_code = TextError.COMMAND_NOT_FOUND

        if is_incoming:
            error = False
            error_code = None

        return TextParserData(
            command=command,
            numbers=numbers,
            names=names,
            number_names=number_names,
            groups=groups,
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

    def get_numbers(self):
        """Search for number."""
        pattern = re.compile(TextRegex.NUMBER)
        search = [x.group() for x in pattern.finditer(self.text)]

        if not search:
            return None

        numbers = []
        for number in search:
            number = re.sub(r"[^\w]", "", number)

            if len(number) == 10:
                number = f"+1{number}"
            elif len(number) == 11:
                number = f"+{number}"
            else:
                number = None

            numbers.append(number)

        return numbers

    def get_names(self):
        pattern = re.compile(TextRegex.NAME)
        search = [x.group() for x in pattern.finditer(self.text)]

        names = []
        for name in search:
            name = name.strip()
            names.append(name)

        return names

    def get_number_names(self):
        pattern = re.compile(TextRegex.NUMBER_NAME)
        search = [x.group() for x in pattern.finditer(self.text)]

        number_names = []
        for number_name in search:
            number_name = number_name.strip()
            number, name = number_name.split(" ")

            number = re.sub(r"[^\w]", "", number)
            if len(number) == 10:
                number = f"+1{number}"
            elif len(number) == 11:
                number = f"+{number}"
            else:
                number = None

            name = name.replace("@", "")

            number_name = (number, name)
            number_names.append(number_name)

        return number_names

    def get_groups(self):
        pattern = re.compile(TextRegex.GROUP)
        search = [x.group() for x in pattern.finditer(self.text)]

        groups = []
        for group in search:
            group = group.strip()
            groups.append(group)

        return groups

    def get_incoming_body(self):
        return self.text

    def get_outgoing_body(self):
        pattern = re.compile(TextRegex.BODY, flags=re.DOTALL)
        search = pattern.search(self.text)

        body = search.group().strip() if search else None

        return body
