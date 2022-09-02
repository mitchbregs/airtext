from airtext.controllers.twilio_webhook import MessageCommand, MessageParserData
from airtext.models.member import Member
from airtext.views.base import View


class IncomingResponse(object):
    ALL = "FROM {number} @{name}\n\n{body_content}"


class OutgoingResponse(object):
    __prehook__ = "FROM @airtext\n\n"

    AIRTEXT = __prehook__ + "About AIRTEXT..."
    ADD_CONTACT = __prehook__ + ("🎉 Added new contact!\n\n{number} @{name}")
    ADD_CONTACT_FAIL = __prehook__ + (
        "🤔 Hmmm, we could not add that contact for you. "
        "Are you sure it does not already exist?\n\n"
        "Try GET {number}."
    )
    GET_CONTACT = __prehook__ + (
        "Found the contact you were looking for! 😎\n\n{number} @{name}"
    )
    GET_CONTACT_FAIL = __prehook__ + (
        "🥸 We were not able to find that contact for you. "
        "Have you tried adding it?\n\n"
        "Try ADD {number}."
    )
    UPDATE_CONTACT = __prehook__ + ("✍️ Updated contact.\n\n{number} @{name}")
    UPDATE_CONTACT_FAIL = __prehook__ + (
        "Couldn't update contact. Are you sure it exists?\n\n" "Try GET {number}."
    )
    DELETE_CONTACT = __prehook__ + ("👻 Deleted contact.\n\n{number} @{name}")
    DELETE_CONTACT_FAIL = __prehook__ + (
        "😵‍💫 Something went wrong trying to delete that contact. "
        "Perhaps you may have not had it in your contact list.\n\n"
        "Try GET {number}."
    )
    COMMAND_NOT_FOUND = __prehook__ + (
        "You either did not provide a command 🤔, or the command you "
        "provided is invalid. 🙅\n\n"
        "The accepted commands are as follows:\n"
        "📲 TO\n"
        "📗 ADD\n"
        "🔎 GET\n"
        "🗑 DELETE\n"
        "📝 UPDATE\n"
    )
    NUMBER_NOT_FOUND = __prehook__ + (
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
    )
    NAME_NOT_FOUND = __prehook__ + (
        "We could not find a name for your contact. 👤\n\n"
        "If you are trying to update a contact, make sure to include their @name.\n\n"
        "For example, UPDATE +19876543210 @JaneDoe."
    )
    BODY_NOT_FOUND = __prehook__ + (
        "🖇  We could not find any text or content to send.\n\n"
        "If you are sending a message to a contact, make sure to include a body of text or something!"
    )

    ERROR_MESSAGES = {
        "command-not-found": COMMAND_NOT_FOUND,
        "number-not-found": NUMBER_NOT_FOUND,
        "name-not-found": NAME_NOT_FOUND,
        "body-not-found": BODY_NOT_FOUND,
    }


class Incoming(View):
    """Handles incoming message end-user result."""

    def __init__(self, member: Member, message: MessageParserData):
        super().__init__(member=member, message=message)

    def send(self):
        """Sends a message and stores record."""
        contact = self.api.contacts.get_by_number_and_member_id(
            number=self.message.from_number, member_id=self.member.id
        )
        name = contact.name if contact else None

        self.api.messages.create(
            from_number=self.message.from_number,
            to_number=self.message.to_number,
            body_content=self.message.body_content,
            media_content=self.message.media_content,
            proxy_number=self.member.proxy_number,
            member_id=self.member.id,
            command=None,
            numbers=[
                self.member.number,
            ],
            names=[],
            groups=[],
            body=IncomingResponse.ALL.format(
                number=self.message.from_number,
                name=name,
                body_content=self.message.body_content,
            ),
            error=False,
            error_code=None,
        )



class Outgoing(View):
    """Handles outgoing message from member."""

    def __init__(self, member: Member, message: MessageParserData):
        super().__init__(member=member, message=message)

    def _run_airtext_command(self):
        self.api.messages.create(
            proxy_number=self.member.proxy_number,
            to_number=self.member.number,
            member_id=self.member.id,
            command=self.message.command,
            numbers=self.message.numbers,
            names=self.message.names,
            groups=self.message.groups,
            body=OutgoingResponse.AIRTEXT,
            error=self.message.error,
            error_code=self.message.error_code,
        )

        return

    def _run_to_command(self):
        self.api.messages.create(
            from_number=self.message.from_number,
            to_number=self.message.to_number,
            body_content=self.message.body_content,
            media_content=self.message.media_content,
            proxy_number=self.member.proxy_number,
            member_id=self.member.id,
            command=self.message.command,
            numbers=self.message.numbers,
            names=self.message.names,
            groups=self.message.groups,
            body=self.message.body,
            error=self.message.error,
            error_code=self.message.error_code,
        )

        return

    def _run_add_command(self):
        # ADD 9086162014
        # ADD 9086162014 @Mitch
        # ADD 9085152013 @John
        # ADD 9086162014 @Mitch,9085152013 @John
        # ADD 9086162014 @Mitch,9085152013

        # CREATE #MyGroup
        # CREATE #MyGroup
        # PUT 9086162014 #MyGroup
        # PUT 9086162014,9085152013 #MyGroup
        # PUT 9086162014,9085152013 #MyGroup
        # ADD @Mitch #MyGroup
        # ADD @Mitch,@John #MyGroup
        # ADD 9086162014 #MyGroup

        contact_identifier

        # If just a number
        if len(self.message.numbers) == 1:
            number = self.message.numbers[0]

        # If just a number and name

        # If just a group

        # If numbers and names, and just a group

        is_added = self.api.contacts.add_contact(
            name=self.message.name,
            number=self.message.number,
            member_id=self.member.id,
        )

        if is_added:
            self.api.messages.create(
                proxy_number=self.member.proxy_number,
                to_number=self.member.number,
                member_id=self.member.id,
                command=self.message.command,
                number=self.message.number,
                name=self.message.name,
                body=OutgoingResponse.ADD_CONTACT.format(
                    number=self.message.number, name=self.message.name
                ),
                error=self.message.error,
                error_code=self.message.error_code,
            )

            return

        self.api.messages.create(
            proxy_number=self.member.proxy_number,
            to_number=self.member.number,
            member_id=self.member.id,
            command=self.message.command,
            number=self.message.number,
            name=self.message.name,
            body=OutgoingResponse.ADD_CONTACT_FAIL.format(
                number=self.message.number, name=self.message.name
            ),
            error=self.message.error,
            error_code=self.message.error_code,
        )

        return

    def _run_get_command(self):
        contact = self.api.contacts.get_by_number_and_member_id(
            number=self.message.number,
            member_id=self.member.id,
        )

        if contact:
            self.api.messages.create(
                proxy_number=self.member.proxy_number,
                to_number=self.member.number,
                member_id=self.member.id,
                command=self.message.command,
                number=self.message.number,
                name=contact.name,
                body=OutgoingResponse.GET_CONTACT.format(
                    number=self.message.number,
                    name=contact.name,
                ),
                error=self.message.error,
                error_code=self.message.error_code,
            )

            return

        self.api.messages.create(
            proxy_number=self.member.proxy_number,
            to_number=self.member.number,
            member_id=self.member.id,
            command=self.message.command,
            number=self.message.number,
            name=self.message.name,
            body=OutgoingResponse.GET_CONTACT_FAIL.format(
                number=self.message.number,
                name=self.message.name,
            ),
            error=self.message.error,
            error_code=self.message.error_code,
        )

        return

    def _run_update_command(self):
        is_updated = self.api.contacts.update_contact(
            number=self.message.number,
            name=self.message.name,
            member_id=self.member.id,
        )

        if is_updated:
            self.api.messages.create(
                proxy_number=self.member.proxy_number,
                to_number=self.member.number,
                member_id=self.member.id,
                command=self.message.command,
                number=self.message.number,
                name=self.message.name,
                body=OutgoingResponse.UPDATE_CONTACT.format(
                    number=self.message.number,
                    name=self.message.name,
                ),
                error=self.message.error,
                error_code=self.message.error_code,
            )

            return

        self.api.messages.create(
            proxy_number=self.member.proxy_number,
            to_number=self.member.number,
            member_id=self.member.id,
            command=self.message.command,
            number=self.message.number,
            name=self.message.name,
            body=OutgoingResponse.UPDATE_CONTACT_FAIL.format(
                number=self.message.number,
                name=self.message.name,
            ),
            error=self.message.error,
            error_code=self.message.error_code,
        )

        return

    def _run_delete_command(self):

        contact = self.api.contacts.get_by_number_and_member_id(
            number=self.message.number, member_id=self.member.id
        )

        is_deleted = self.api.contacts.delete_contact(
            number=self.message.number,
            member_id=self.member.id,
        )

        if contact and is_deleted:
            self.api.messages.create(
                proxy_number=self.member.proxy_number,
                to_number=self.member.number,
                member_id=self.member.id,
                command=self.message.command,
                number=self.message.number,
                name=contact.name,
                body=OutgoingResponse.DELETE_CONTACT.format(
                    number=self.message.number,
                    name=contact.name,
                ),
                error=self.message.error,
                error_code=self.message.error_code,
            )

            return

        self.api.messages.create(
            proxy_number=self.member.proxy_number,
            to_number=self.member.number,
            member_id=self.member.id,
            command=self.message.command,
            number=self.message.number,
            name=self.message.name,
            body=OutgoingResponse.DELETE_CONTACT_FAIL.format(
                number=self.message.number,
                name=self.message.name,
            ),
            error=self.message.error,
            error_code=self.message.error_code,
        )

        return

    def _run_error(self, **kwargs):

        self.api.messages.create(
            proxy_number=self.member.proxy_number,
            to_number=self.member.number,
            member_id=self.member.id,
            command=self.message.command,
            number=self.message.number,
            name=self.message.name,
            body=OutgoingResponse.ERROR_MESSAGES[self.message.error_code],
            error=self.message.error,
            error_code=self.message.error_code,
        )

        return

    def send(self):
        """Sends a message and stores record."""
        if self.message.error:
            self._run_error()
        elif self.message.command.upper() == MessageCommand.AIRTEXT:
            self._run_airtext_command()
        elif self.message.command.upper() == MessageCommand.TO:
            self._run_to_command()
        elif self.message.command.upper() == MessageCommand.ADD:
            self._run_add_command()
        elif self.message.command.upper() == MessageCommand.GET:
            self._run_get_command()
        elif self.message.command.upper() == MessageCommand.UPDATE:
            self._run_update_command()
        elif self.message.command.upper() == MessageCommand.DELETE:
            self._run_delete_command()
        elif self.message.command.upper() == MessageCommand.PUT:
            self._run_put_command()
        elif self.message.command.upper() == MessageCommand.REMOVE:
            self._run_remove_command()
        else:
            return False

        return True
