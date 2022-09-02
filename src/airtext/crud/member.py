from airtext.crud.base import DatabaseMixin
from airtext.models.member import Member


class MemberAPI(DatabaseMixin):
    def create(self, proxy_number: str, name: str, email: str, number: str):
        with self.database() as session:
            member = Member(
                proxy_number=proxy_number,
                name=name,
                email=email,
                number=number,
            )
            session.add(member)
            session.refresh(member)
            session.commit()

        return member

    def get_by_id(self, id: int):
        with self.database() as session:
            return session.query(Member).filter_by(id=id).one()

    def get_by_proxy_number(self, proxy_number: str):
        with self.database() as session:
            return session.query(Member).filter_by(proxy_number=proxy_number).one()
