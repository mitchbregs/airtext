from airtext.controllers.parser import MessageCommand, MessageParserData
from airtext.models.member import Member
from airtext.views.base import View
from airtext.views.response import OutgoingResponse


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
