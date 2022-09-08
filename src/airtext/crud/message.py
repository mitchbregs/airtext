from sqlalchemy import asc, text
from sqlalchemy.sql.expression import literal

from airtext.crud.base import DatabaseMixin
from airtext.crud.contact import ContactAPI
from airtext.crud.group_contact import GroupContactAPI
from airtext.crud.twilio import TwilioAPI
from airtext.models.member import Member
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
        number_names: list,
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
                member_id=member_id,
            )

            for group_contact in contact_list:
                numbers.append(group_contact.get("number"))

        twilio_api = TwilioAPI()
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
                    number_names=number_names,
                    groups=groups,
                    body=body,
                    error=error,
                    error_code=error_code,
                )
                messages.append(message)

                twilio_api.create_message(
                    to_number=number,
                    proxy_number=proxy_number,
                    body=body,
                    media_url=media_content,
                )

                session.add(message)
                session.commit()
                session.refresh(message)

        return message

    def get_by_number_and_member_id(self, number: str, member_id: int):
        """Gets a conversation."""
        # -- Gets incoming messages
        # select
        #     created_on,
        #     number as from_number,
        #     to_number as to_number,
        #     body as body,
        #     media_content as media_url,
        #     true as is_incoming
        # from messages
        # where number = :number -- from_number
        # and to_number = (
        #     select proxy_number
        #     from members
        #     where id = :member_id
        # ) -- proxy_number
        # union
        # -- Gets outgoing messages, yes it's weird
        # select
        #     created_on,
        #     to_number as from_number,
        #     from_number as to_number,
        #     body_content as body,
        #     media_content as media_url,
        #     false as is_incoming
        # from messages
        # where from_number = :number -- from_number
        # and to_number = (
        #     select proxy_number
        #     from members
        #     where id = :member_id
        # ) -- proxy_number
        # order by created_on
        with self.database() as session:
            proxy_number = (
                session.query(Member.proxy_number)
                .filter_by(id=member_id)
                .scalar_subquery()
            )
            incoming = (
                session.query(
                    Message.created_on.label("created_on"),
                    Message.number.label("from_number"),
                    Message.to_number.label("to_number"),
                    Message.body.label("body"),
                    Message.media_content.label("media_url"),
                    literal(True).label("is_incoming"),
                )
                .filter_by(
                    number=number,
                    to_number=proxy_number
                )
            )
            outgoing = (
                session.query(
                    Message.created_on.label("created_on"),
                    Message.to_number.label("from_number"),
                    Message.from_number.label("to_number"),
                    Message.body_content.label("body"),
                    Message.media_content.label("media_url"),
                    literal(False).label("is_incoming"),
                )
                .filter_by(
                    from_number=number,
                    to_number=proxy_number
                )
            )
            messages = [
                dict(x) for x in (
                    incoming.union(outgoing)
                    .order_by(asc(Message.created_on))
                    .all()
                )
            ]

        return messages
