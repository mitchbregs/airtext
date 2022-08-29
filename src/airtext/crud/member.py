from airtext.crud.base import ExternalConnectionsMixin
from airtext.models.member import Member


class MemberAPI(ExternalConnectionsMixin):
    def get_by_proxy_number(self, proxy_number: str):
        with self.database() as session:
            return session.query(Member).filter_by(proxy_number=proxy_number).one()
