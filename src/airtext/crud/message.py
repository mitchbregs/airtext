from airtext.crud.base import DatabaseMixin
from airtext.crud.twilio import TwilioAPI
from airtext.models.message import Message


class MessageAPI(DatabaseMixin):

    def create(
        self,
        to_number: str,
        from_number: str,
        body: str,
        media_url: str,
        member_id: str,
        subaccount_sid: str = None,
    ):
        client = TwilioAPI()
        if subaccount_sid:
            subaccount = client.get_subaccount(subaccount_sid)
            client = client.get_subaccount_client(
                sid=subaccount.sid,
                auth_token=subaccount.auth_token
            )

        twilio_message = client.create_message(
            to_number=to_number,
            from_number=from_number,
            body=body,
            media_url=media_url,
        )

        with self.database() as session:
            message = Message(
                member_id=member_id,
                to_number=to_number,
                from_number=from_number,
                body=body,
                media_url=media_url,
                twilio_message_sid=twilio_message.sid,
                twilio_uri=twilio_message.uri,
                twilio_error_code=twilio_message.error_code,
                twilio_error_message=twilio_message.error_message,
            )
            session.add(message)
            session.commit()
            session.refresh(message)

        return message
