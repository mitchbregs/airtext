import re
from dataclasses import dataclass
from typing import List, Optional, Pattern, Tuple
from urllib.parse import unquote_plus

from pydantic import BaseModel

from airtext.controllers.base import RequestData


class MessageRegex:
    COMMAND = r"^(TO|CREATE|GET|UPDATE|DELETE|ADD|REMOVE)"
    NUMBER = r"(\+\d{1,2}\s?)?1?\-?\.?\s?\(?\d{3}\)?[\s.-]?\d{3}[\s.-]?\d{4}"
    NAME = r"(?<=@)(.*?)(?=\,|$|\s+|\:|\;)"
    GROUP = r"(?<=#)(.*?)(?=\,|$|\s+|\:|\;)"
    BODY_CONTENT = r"\n(.*)?"


class MessageCommand:
    TO: str = "TO"
    CREATE: str = "CREATE"
    GET: str = "GET"
    UPDATE: str = "UPDATE"
    DELETE: str = "DELETE"
    ADD: str = "ADD"
    REMOVE: str = "REMOVE"


class MessageContact(BaseModel):
    number: Optional[str]
    name: Optional[str]


class MessageGroup(BaseModel):
    name: str


class MessageData(RequestData):
    command: Optional[str]
    contacts: Optional[List[MessageContact]]
    groups: Optional[List[MessageGroup]]
    body_content: Optional[str]
    error: Optional[bool]
    error_message: Optional[str]


class MessageParser:
    def __init__(self, event: dict):
        self.to_number = unquote_plus(event["To"])
        self.from_number = unquote_plus(event["From"])
        self.body = unquote_plus(event["Body"])
        # TODO: Handle multiple media urls
        self.media_url = (
            unquote_plus(event.get("MediaUrl0")) if event.get("MediaUrl0") else None
        )

    def parse(self):
        command = self.get_command()

        if command:
            command = command.upper()
            error = False
            error_message = None
        else:
            error = True
            error_message = "No command found."

        params = self.get_params()

        if command == MessageCommand.TO:
            if not (len(params["contacts"]) > 0 or len(params["groups"]) > 0):
                error = True
                error_message = "Missing a contact or group to send message."
            elif not (params["body_content"] or self.media_url):
                error = True
                error_message = "Missing message content to send."

        if command == MessageCommand.CREATE:
            if not (len(params["contacts"]) > 0 or len(params["groups"]) > 0):
                error = True
                error_message = "Missing contact(s) or group(s) to create."

        if command == MessageCommand.GET:
            if not (len(params["contacts"]) > 0 or len(params["groups"]) > 0):
                error = True
                error_message = "Missing contact(s) or group(s) to get."

        if command == MessageCommand.UPDATE:
            if not len(params["contacts"]) > 0:
                error = True
                error_message = "Missing contact(s) to update."

        if command == MessageCommand.DELETE:
            if not (len(params["contacts"]) > 0 or len(params["groups"]) > 0):
                error = True
                error_message = "Missing contact(s) or group(s) to delete."

        if command == MessageCommand.ADD:
            if not len(params["contacts"]) > 0:
                error = True
                error_message = "Missing contact(s) to add to group."
            elif len(params["groups"]) != 1:
                error = True
                error_message = "Must include only 1 group to add contacts to."

        if command == MessageCommand.REMOVE:
            if not len(params["contacts"]) > 0:
                error = True
                error_message = "Missing contact(s) to remove from group."
            elif len(params["groups"]) != 1:
                error = True
                error_message = "Must include only 1 group to remove contacts from."

        return MessageData(
            to_number=self.to_number,
            from_number=self.from_number,
            body=self.body,
            media_url=self.media_url,
            command=command,
            **params,
            error=error,
            error_message=error_message,
        )

    def search(self, pattern: Pattern, string: str, flags: re.enum.Flag = 0):
        prog = re.compile(pattern=pattern, flags=flags)
        result = prog.search(string)
        return result.group() if result else None

    def get_command(self):
        """Search for the command."""
        return self.search(
            pattern=MessageRegex.COMMAND, string=self.body, flags=re.IGNORECASE
        )

    def get_params(self):
        body = re.sub(MessageRegex.COMMAND, "", self.body)
        arguments = [x.strip() for x in body.split(",")]
        params = {"contacts": [], "groups": [], "body_content": None}

        for argument in arguments:
            contact_number = self.search(pattern=MessageRegex.NUMBER, string=argument)
            contact_name = self.search(pattern=MessageRegex.NAME, string=argument)
            group_name = self.search(pattern=MessageRegex.GROUP, string=argument)

            if contact_number:
                number = re.sub(r"[^\w]", "", contact_number)
                if len(number) == 10:
                    number = f"+1{number}"
                elif len(number) == 11:
                    number = f"+{number}"
                else:
                    raise Exception

                request_contact = MessageContact(number=number, name=contact_name)
                params["contacts"].append(request_contact)

            elif contact_name:
                request_contact = MessageContact(
                    number=contact_number, name=contact_name
                )
                params["contacts"].append(request_contact)

            if group_name:
                request_group = MessageGroup(name=group_name)
                params["groups"].append(request_group)

        body_content = self.search(
            pattern=MessageRegex.BODY_CONTENT, string=body, flags=re.DOTALL
        )
        params["body_content"] = body_content.strip() if body_content else None

        return params
