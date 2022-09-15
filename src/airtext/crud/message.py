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
        body: str,
        media_url: str,
        proxy_number: str,
        member_id: int,
        command: str,
        contacts: list,
        groups: list,
        body_content: str,
        error: bool,
        error_message: str,
    ):
        twilio = TwilioAPI()
        twilio_message = twilio.create_message(
            to_number=to_number,
            proxy_number=proxy_number,
            body=body,
            media_url=media_url,
        )

        with self.database() as session:
            message = Message(
                to_number=to_number,
                from_number=from_number,
                body=body,
                media_url=media_url,
                proxy_number=proxy_number,
                member_id=member_id,
                command=command,
                contacts=contacts,
                groups=groups,
                body_content=body_content,
                error=error,
                error_message=error_message,
                twilio_uri=twilio_message.uri,
                twilio_error_code=twilio_message.error_code,
                twilio_error_message=twilio_message.error_message,
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
            incoming = session.query(
                Message.created_on.label("created_on"),
                Message.from_number.label("from_number"),
                Message.to_number.label("to_number"),
                Message.body.label("body"),
                Message.media_url.label("media_url"),
                literal(True).label("is_incoming"),
            ).filter_by(from_number=number, to_number=proxy_number)
            outgoing = session.query(
                Message.created_on.label("created_on"),
                Message.to_number.label("from_number"),
                Message.from_number.label("to_number"),
                Message.body_content.label("body"),
                Message.media_url.label("media_url"),
                literal(False).label("is_incoming"),
            ).filter_by(from_number=proxy_number, to_number=number)
            messages = [
                dict(x)
                for x in (
                    incoming.union(outgoing).order_by(asc(Message.created_on)).all()
                )
            ]

        return messages
