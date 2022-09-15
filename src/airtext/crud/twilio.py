from airtext.crud.base import TwilioMixin
from airtext.models.contact import Contact
from airtext.models.group import Group
from airtext.models.group_contact import GroupContact


class TwilioAPI(TwilioMixin):
    def create_number(self, area_code: str = None):
        phone = self.twilio.incoming_phone_numbers.create(area_code=area_code)
        phone.update(
            sms_method="POST",
            sms_url="https://72cnwtckz5.execute-api.us-east-1.amazonaws.com/v1/message",
        )

        return phone

    def create_message(
        self, to_number: str, proxy_number: str, body: str, media_url: str
    ):
        return self.twilio.messages.create(
            to=to_number,
            from_=proxy_number,
            body=body,
            media_url=media_url,
        )
