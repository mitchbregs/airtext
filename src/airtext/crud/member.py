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
            session.commit()
            session.refresh(member)

        return member

    def get_by_id(self, id: int):
        with self.database() as session:
            return session.query(Member).filter_by(id=id).one()

    def get_by_proxy_number(self, proxy_number: str):
        with self.database() as session:
            return session.query(Member).filter_by(proxy_number=proxy_number).one()

    def delete(self, id: int):
        with self.database() as session:
            member = session.query(Member).filter_by(id=id).one()
            session.delete(member)
            session.commit()

        return member
