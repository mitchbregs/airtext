from airtext.api import AirtextAPI
from airtext.models.member import Member
from airtext.views.base import View
from airtext.views.response import OutgoingResponse


class Outgoing(View):
    """Handles outgoing message from member."""

    def __init__(self, member: Member, text: str):
        self.member = member
        self.text = text
        self.api = AirtextAPI()

    def _run_airtext_command(self):
        self.api.messages.create(
            proxy_number=self.member.proxy_number,
            to_number=self.member.number,
            member_id=self.member.id,
            command=self.text.command,
            number=self.text.number,
            name=self.text.name,
            body=self.text.body,
            error=self.text.error,
            error_code=self.text.error_code,
        )

        return

    def _run_to_command(self):
        self.api.messages.create(
            proxy_number=self.member.proxy_number,
            to_number=self.text.number,  # NOTE: Truly outgoing
            member_id=self.member.id,
            command=self.text.command,
            number=self.text.number,
            name=self.text.name,
            body=self.text.body,
            error=self.text.error,
            error_code=self.text.error_code,
        )

        return

    def _run_add_command(self):

        is_added = self.api.contacts.add_contact(
            name=self.text.name,
            number=self.text.number,
            member_id=self.member.id,
        )

        if is_added:
            self.api.messages.create(
                proxy_number=self.member.proxy_number,
                to_number=self.member.number,
                member_id=self.member.id,
                command=self.text.command,
                number=self.text.number,
                name=self.text.name,
                body=OutgoingResponse.ADD_CONTACT.format(
                    number=self.text.number, name=self.text.name
                ),
                error=self.text.error,
                error_code=self.text.error_code,
            )

            return

        self.api.messages.create(
            proxy_number=self.member.proxy_number,
            to_number=self.member.number,
            member_id=self.member.id,
            command=self.text.command,
            number=self.text.number,
            name=self.text.name,
            body=OutgoingResponse.ADD_CONTACT_FAIL.format(
                number=self.text.number, name=self.text.name
            ),
            error=self.text.error,
            error_code=self.text.error_code,
        )

        return

    def _run_get_command(self):
        if self.text.number:
            contact = self.api.contacts.get_by_number_and_member_id(
                number=self.text.number,
                member_id=self.member.id,
            )
        elif self.text.name:
            contact = self.api.contacts.get_by_name_and_member_id(
                name=self.text.name,
                member_id=self.member.id,
            )

        name = contact.name if contact else None

        if contact:
            self.api.messages.create(
                proxy_number=self.member.proxy_number,
                to_number=self.member.number,
                member_id=self.member.id,
                command=self.text.command,
                number=self.text.number,
                name=contact.name,
                body=OutgoingResponse.GET_CONTACT.format(
                    number=self.text.number,
                    name=self.text.name,
                ),
                error=self.text.error,
                error_code=self.text.error_code,
            )

            return

        self.api.messages.create(
            proxy_number=self.member.proxy_number,
            to_number=self.member.number,
            member_id=self.member.id,
            command=self.text.command,
            number=self.text.number,
            name=self.text.name,
            body=OutgoingResponse.GET_CONTACT_FAIL.format(
                number=self.text.number,
                name=self.text.name,
            ),
            error=self.text.error,
            error_code=self.text.error_code,
        )

        return

    def _run_update_command(self):
        is_updated = self.api.contacts.update_contact(
            number=self.text.number,
            name=self.text.name,
            member_id=self.member.id,
        )

        if is_updated:
            self.api.messages.create(
                proxy_number=self.member.proxy_number,
                to_number=self.member.number,
                member_id=self.member.id,
                command=self.text.command,
                number=self.text.number,
                name=self.text.name,
                body=OutgoingResponse.UPDATE_CONTACT.format(
                    number=self.text.number,
                    name=self.text.name,
                ),
                error=self.text.error,
                error_code=self.text.error_code,
            )

            return

        self.api.messages.create(
            proxy_number=self.member.proxy_number,
            to_number=self.member.number,
            member_id=self.member.id,
            command=self.text.command,
            number=self.text.number,
            name=self.text.name,
            body=OutgoingResponse.UPDATE_CONTACT_FAIL.format(
                number=self.text.number,
                name=self.text.name,
            ),
            error=self.text.error,
            error_code=self.text.error_code,
        )

        return

    def _run_delete_command(self):
        is_deleted = self.api.contacts.delete_contact(
            number=self.text.number,
            member_id=self.member.id,
        )

        if is_deleted:
            self.api.messages.create(
                proxy_number=self.member.proxy_number,
                to_number=self.member.number,
                member_id=self.member.id,
                command=self.text.command,
                number=self.text.number,
                name=self.text.name,
                body=OutgoingResponse.DELETE_CONTACT.format(
                    number=self.text.number,
                    name=self.text.name,
                ),
                error=self.text.error,
                error_code=self.text.error_code,
            )

            return

        self.api.messages.create(
            proxy_number=self.member.proxy_number,
            to_number=self.member.number,
            member_id=self.member.id,
            command=self.text.command,
            number=self.text.number,
            name=self.text.name,
            body=OutgoingResponse.DELETE_CONTACT_FAIL.format(
                number=self.text.number,
                name=self.text.name,
            ),
            error=self.text.error,
            error_code=self.text.error_code,
        )

        return

    def _run_error(self, **kwargs):

        self.api.messages.create(
            proxy_number=self.member.proxy_number,
            to_number=self.member.number,
            member_id=self.member.id,
            command=self.text.command,
            number=self.text.number,
            name=self.text.name,
            body=OutgoingResponse.ERROR_MESSAGES[self.text.error_code],
            error=self.text.error,
            error_code=self.text.error_code,
        )

        return

    def send(self):
        """Sends a message and stores record."""
        if self.text.error:
            self._run_error()
        elif self.text.command.upper() == "AIRTEXT":
            self._run_airtext_command()
        elif self.text.command.upper() == "TO":
            self._run_to_command()
        elif self.text.command.upper() == "ADD":
            self._run_add_command()
        elif self.text.command.upper() == "GET":
            self._run_get_command()
        elif self.text.command.upper() == "UPDATE":
            self._run_update_command()
        elif self.text.command.upper() == "DELETE":
            self._run_delete_command()
        else:
            return False

        return True
