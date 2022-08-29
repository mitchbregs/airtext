from airtext.crud.base import ExternalConnectionsMixin
from airtext.crud.contact import ContactAPI
from airtext.crud.group_contact import GroupContactAPI
from airtext.models.message import Message


class MessageAPI(ExternalConnectionsMixin):
    def create(
        self,
        proxy_number: str,
        member_id: int,
        command: str,
        numbers: list,
        names: list,
        groups: list,
        body: str,
        error: bool,
        error_code: bool,
    ):
        number_list = numbers

        contacts_api = ContactAPI()
        for name in names:
            contact = contacts_api.get_by_name_and_member_id(
                name=name, member_id=member_id
            )

            if contact:
                number_list.append(contact.number)

        group_contacts_api = GroupContactAPI()
        group_contacts = []
        for group in groups:
            contact_list = group_contacts_api.get_by_name_and_member_id(
                name=group,
                member_id=membeR_id,
            )

            for group_contact in contact_list:
                number_list.append(group_contact.get("number"))

        with self.database() as session:
            messages = []
            for number in number_list:
                message = Message(
                    proxy_number=proxy_number,
                    to_number=number,
                    member_id=member_id,
                    command=command,
                    numbers=numbers,
                    names=names,
                    groups=groups,
                    body=body,
                    error=error,
                    error_code=error_code,
                )
                messages.append(message)

            session.add(message)
            session.commit()

        for number in number_list:
            self.twilio.messages.create(
                to=number,
                from_=proxy_number,
                body=body,
            )

        return True
