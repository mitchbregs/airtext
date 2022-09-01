from airtext.crud.base import ExternalConnectionsMixin
from airtext.models.contact import Contact
from airtext.models.member import Member


class ContactAPI(ExternalConnectionsMixin):
    def create(self, number: str, member_id: int, name: str = None):
        with self.database() as session:
            contact = Contact(
                number=number,
                member_id=member_id,
                name=name,
            )
            session.add(contact)
            session.commit()

        return

    def get_by_proxy_number(self, proxy_number: str):
        with self.database() as session:
            return (
                session.query(Contact)
                    .join(Member)
                    .filter_by(proxy_number=proxy_number).all()
            )

    def get_by_name_and_member_id(self, name: str, member_id: int):
        with self.database() as session:
            return (
                session.query(Contact)
                .filter_by(
                    name=name,
                    member_id=member_id,
                )
                .first()
            )

    def get_by_number_and_member_id(self, number: str, member_id: int):
        with self.database() as session:
            return (
                session.query(Contact)
                .filter_by(
                    number=number,
                    member_id=member_id,
                )
                .first()
            )

    def update(self, number: str, member_id: int, name: str):
        with self.database() as session:
            contact = (
                session.query(Contact)
                .filter_by(
                    number=number,
                    member_id=member_id,
                )
                .first()
            )
            contact.name = name
            session.commit()

        return

    def delete(self, number: str, member_id: int):
        with self.database() as session:
            contact = (
                session.query(Contact)
                .filter_by(
                    number=number,
                    member_id=member_id,
                )
                .first()
            )
            session.delete(contact)
            session.commit()

        return
