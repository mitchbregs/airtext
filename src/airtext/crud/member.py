from airtext.crud.base import ExternalConnectionsMixin
from airtext.models.member import Member


class MemberAPI(ExternalConnectionsMixin):
    def create(self, name: str, email: str, number: str, area_code: str = None):
        area_code = area_code if area_code else number[2:5]
        phone = self.twilio.incoming_phone_numbers.create(area_code=area_code)
        phone.update(
            sms_method='POST',
            sms_url='https://z4muss792f.execute-api.us-east-1.amazonaws.com/dev/twilio-webhook',
        )

        with self.database() as session:
            member = Member(
                proxy_number=phone.phone_number,
                name=name,
                email=email,
                number=number,
            )
            session.add(member)
            session.commit()

        return

    def get_by_proxy_number(self, proxy_number: str):
        with self.database() as session:
            return session.query(Member).filter_by(proxy_number=proxy_number).one()
