from twilio.rest import Client

from airtext.config import TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN


class TwilioAPI:
    def __init__(self):
        self.twilio = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

    def create_subaccount(self, name: str):
        return self.twilio.api.v2010.accounts.create(friendly_name=name)

    def get_subaccount(self, sid: str):
        return self.twilio.api.v2010.accounts(sid).fetch()

    def get_subaccount_client(self, sid, auth_token):
        return Client(sid, auth_token)

    def suspend_subaccount(self, sid: str):
        return self.twilio.api.v2010.accounts(sid).update(status="suspend")

    def activate_subaccount(self, sid: str):
        return self.twilio.api.v2010.accounts(sid).update(status="active")

    def delete_subaccount(self, sid: str):
        return self.twilio.api.v2010.accounts(sid).update(status="closed")

    def search_numbers(self, area_code: str = None):
        numbers = self.twilio.available_phone_numbers('US').local.list(
            area_code=area_code,
            limit=20,
            sms_enabled=True,
            mms_enabled=True,
        )

        return [num.phone_number for num in numbers]

    def create_number(self, phone_number: str, subaccount_sid: str = None):
        subaccount = self.get_subaccount(subaccount_sid)
        client = self.get_subaccount_client(sid=subaccount.sid, auth_token=subaccount.auth_token)
        phone = client.create(
            phone_number=phone_number,
            sms_method="POST",
            sms_url="https://72cnwtckz5.execute-api.us-east-1.amazonaws.com/v1/message",
        )

        return phone

    def send_message(
        self, to_number: str, from_number: str, body: str, media_url: str
    ):
        return self.twilio.messages.create(
            to=to_number,
            from_=from_number,
            body=body,
            media_url=media_url,
        )
