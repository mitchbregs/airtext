from twilio.rest import Client

from airtext.api import AirtextAPI
from airtext.config import TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN


class AirtextProxy:
    def __init__(self, proxy_number: str, from_number: str, text: str):
        self.proxy_number = proxy_number
        self.from_number = from_number
        self.text = text

        self.member = self.get_member()

    @property
    def contact(self):
        return self.get_contact()

    @property
    def api(self) -> AirtextAPI:
        return AirtextAPI()

    def __repr__(self):
        return f"<AirtextProxy proxy_number={self.proxy_number}>"

    def get_member(self):
        return self.api.members.get_by_proxy_number(proxy_number=self.proxy_number)

    def get_contact(self):
        return self.api.contacts.get_by_number_and_member_id(
            number=self.from_number, member_id=self.member.id
        )

    def send(self, to: str, body: str):
        client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
        client.messages.create(
            to=to,
            from_=self.member.proxy_number,
            body=body,
        )

        return True
