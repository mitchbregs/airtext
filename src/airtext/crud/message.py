from airtext.crud.base import DatabaseMixin
from airtext.crud.contact import ContactAPI
from airtext.crud.group_contact import GroupContactAPI
from airtext.models.message import Message


class MessageAPI(DatabaseMixin):
    def create(
        self,
        to_number: str,
        from_number: str,
        body_content: str,
        media_content: str,
        proxy_number: str,
        member_id: int,
        command: str,
        numbers: list,
        names: list,
        groups: list,
        body: str,
        error: bool,
        error_code: str,
    ):
        contacts_api = ContactAPI()
        for name in names:
            contact = contacts_api.get_by_name_and_member_id(
                name=name, member_id=member_id
            )

            if contact:
                numbers.append(contact.number)

        group_contacts_api = GroupContactAPI()
        group_contacts = []
        for group in groups:
            contact_list = group_contacts_api.get_by_name_and_member_id(
                name=group,
                member_id=membeR_id,
            )

            for group_contact in contact_list:
                numbers.append(group_contact.get("number"))

        with self.database() as session:
            messages = []

            for number in numbers:
                message = Message(
                    to_number=to_number,
                    from_number=from_number,
                    body_content=body_content,
                    media_content=media_content,
                    proxy_number=proxy_number,
                    number=number,
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

                self.twilio.messages.create(
                    to=number,
                    from_=proxy_number,
                    body=body,
                    media_url=media_content,
                )

                session.add(message)
                session.refresh(message)
                session.commit()

        return message

    def get_by_proxy_number(self, proxy_number: str):
        with self.database() as session:
            return (
                session.query(Message)
                .filter_by(proxy_number=proxy_number)
                .order_by(Message.created_on)
                .all()
            )
