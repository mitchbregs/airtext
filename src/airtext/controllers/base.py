from abc import ABC, abstractmethod
from airtext.api import AirtextAPI


class Controller(ABC):
    def __init__(self, request: Request):
        self.request = request
        self.api = AirtextAPI()

    @abstractmethod
    def dispatch_request(self):
        pass


class Request:
    def __init__(self, event: dict):
        self.event = event

    def parse_message(self):
        parser = RequestParser(event=self.event)
        message = parser.parse()
        return message



class RequestRegex:
    COMMAND = r"^(AIRTEXT|TO|ADD|GET|UPDATE|DELETE|CREATE|PUT|REMOVE)"
    NUMBER = r"(\+\d{1,2}\s?)?1?\-?\.?\s?\(?\d{3}\)?[\s.-]?\d{3}[\s.-]?\d{4}"
    NAME = r"(?<=@)(.*?)(?=\,|$|\s+|\:|\;)"
    NUMBER_NAME = r"(\+\d{1,2}\s?)?1?\-?\.?\s?\(?\d{3}\)?[\s.-]?\d{3}[\s.-]?\d{4}\s+(?=@)(.*?)(?=\,|$|\s+|\:|\;)"
    GROUP = r"(?<=#)(.*?)(?=\,|$|\s+|\:|\;)"
    BODY = r"\n(.*)?"


class RequestCommand:
    AIRTEXT: str = "AIRTEXT"
    TO: str = "TO"
    ADD: str = "ADD"
    GET: str = "GET"
    UPDATE: str = "UPDATE"
    DELETE: str = "DELETE"
    CREATE: str = "CREATE"
    PUT: str = "PUT"
    REMOVE: str = "REMOVE"


class RequestError:
    COMMAND_NOT_FOUND: str = "command-not-found"
    NUMBER_NOT_FOUND: str = "number-not-found"
    NAME_NOT_FOUND: str = "name-not-found"
    NUMBER_NAME_NOT_FOUND: str = "number-name-not-found"
    GROUP_NOT_FOUND: str = "group-not-found"
    BODY_NOT_FOUND: str = "body-not-found"


@dataclass
class RequestParserData:
    to_number: str
    from_number: str
    body_content: str
    media_content: str
    command: str
    numbers: List[str]
    names: List[str]
    number_names: List[Tuple]
    groups: List[str]
    body: str
    error: bool
    error_code: str


class RequestParser:
    def __init__(self, event: str):
        self.to_number = unquote_plus(event["To"])
        self.from_number = unquote_plus(event["From"])
        self.body_content = unquote_plus(event["Body"])
        media_url = event.get("MediaUrl0")  # TODO: Handle multiple
        self.media_content = unquote_plus(media_url) if media_url else None

    def parse(self):
        command = self.get_command()
        numbers = self.get_numbers()
        names = self.get_names()
        number_names = self.get_number_names()
        groups = self.get_groups()
        body = self.get_body()
        error = False
        error_code = None

        if command == RequestCommand.AIRTEXT:
            error = False
            error_code = None
        elif command == RequestCommand.TO:
            if not any([numbers, names, groups]):
                error = True
                error_code = RequestError.NUMBER_NOT_FOUND
            # TODO: handle body vs url
            elif not body:
                error = True
                error_code = RequestError.BODY_NOT_FOUND
        elif command == RequestCommand.ADD:
            if not any([numbers, names, number_names]):
                error = True
                error_code = RequestError.NUMBER_NOT_FOUND
        elif command == RequestCommand.GET:
            if not any([numbers, names, groups]):
                error = True
                error_code = RequestError.GROUP_NOT_FOUND
        elif command == RequestCommand.UPDATE:
            if not numer_names:
                error = True
                error_code = RequestError.NUMBER_NAME_NOT_FOUND
        elif command == RequestCommand.DELETE:
            if not any([numbers, names, groups]):
                error = True
                error_code = RequestError.NUMBER_NOT_FOUND
        elif command == RequestCommand.CREATE:
            if not group:
                error = True
                error_code = RequestError.GROUP_NOT_FOUND
        elif command == RequestCommand.PUT:
            if not any([numbers, names]):
                error = True
                error_code = RequestError.NUMBER_NOT_FOUND
            if not groups:
                error = True
                error_code = RequestError.GROUP_NOT_FOUND
        elif command == RequestCommand.REMOVE:
            if not any([numbers, names]):
                error = True
                error_code = RequestError.NUMBER_NOT_FOUND
            if not groups:
                error = True
                error_code = RequestError.GROUP_NOT_FOUND
        else:
            error = True
            error_code = RequestError.COMMAND_NOT_FOUND

        return RequestParserData(
            to_number=self.to_number,
            from_number=self.from_number,
            body_content=self.body_content,
            media_content=self.media_content,
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
        pattern = re.compile(RequestRegex.COMMAND, re.IGNORECASE)
        search = pattern.search(self.body_content)

        command = search.group() if search else None

        return command

    def get_numbers(self):
        """Search for number."""
        pattern = re.compile(RequestRegex.NUMBER)
        search = [x.group() for x in pattern.finditer(self.body_content)]

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
        pattern = re.compile(RequestRegex.NAME)
        search = [x.group() for x in pattern.finditer(self.body_content)]

        names = []
        for name in search:
            name = name.strip()
            names.append(name)

        return names

    def get_number_names(self):
        pattern = re.compile(RequestRegex.NUMBER_NAME)
        search = [x.group() for x in pattern.finditer(self.body_content)]

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
        pattern = re.compile(RequestRegex.GROUP)
        search = [x.group() for x in pattern.finditer(self.body_content)]

        groups = []
        for group in search:
            group = group.strip()
            groups.append(group)

        return groups

    def get_body(self):
        pattern = re.compile(RequestRegex.BODY, flags=re.DOTALL)
        search = pattern.search(self.body_content)

        body = search.group().strip() if search else None

        return body
