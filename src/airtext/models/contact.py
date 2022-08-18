from airtext.models.base import Contact
from airtext.models.mixin import ExternalConnectionsMixin


class ContactAPI(ExternalConnectionsMixin):
    def add_contact(self, name: str, number: str, member_id: int):
        with self.database() as session:
            contact = Contact(
                name=name,
                number=number,
                member_id=member_id,
            )
            session.add(contact)
            try:
                session.commit()
            except IntegrityError:
                return False

        return True

    def get_by_proxy_number(self, proxy_number: str):
        with self.database() as session:
            return session.query(Contact).filter_by(proxy_number=proxy_number).all()

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

    def update_contact(self, number: str, name: str, member_id: int):
        with self.database() as session:
            contact = (
                session.query(Contact)
                .filter_by(
                    number=number,
                    member_id=member_id,
                )
                .first()
            )

            if contact:
                contact.name = name
                session.commit()

                return True

        return False

    def delete_contact(self, number: str, member_id: int):
        with self.database() as session:
            contact = (
                session.query(Contact)
                .filter_by(
                    number=number,
                    member_id=member_id,
                )
                .first()
            )

            if contact:
                session.delete(contact)
                session.commit()

                return True

        return False
