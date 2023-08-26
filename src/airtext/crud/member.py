from airtext.crud.base import DatabaseMixin
from airtext.models.member import Member


class MemberAPI(DatabaseMixin):
    def create(self, first_name: str, last_name: str, email: str, phone_number: str):
        with self.database() as session:
            member = Member(
                first_name=first_name,
                last_name=last_name,
                email=email,
                phone_number=phone_number,
            )
            session.add(member)
            session.commit()
            session.refresh(member)

        return member

    def get_by_id(self, id: int):
        with self.database() as session:
            return session.query(Member).filter_by(id=id).one()

    def get_by_email(self, email: str):
        with self.database() as session:
            return session.query(Member).filter_by(email=email).one()

    def get_by_phone_number(self, phone_number: str):
        with self.database() as session:
            return session.query(Member).filter_by(phone_number=phone_number).one()

    def delete(self, phone_number: int):
        with self.database() as session:
            member = session.query(Member).filter_by(id=id).one()
            session.delete(member)
            session.commit()

        return member
