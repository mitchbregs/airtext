from airtext.crud.base import DatabaseMixin
from airtext.models.contact import Contact


class ContactAPI(DatabaseMixin):

    def create(self, member_id: str, number: str, first_name: str, last_name: str):
        with self.database() as session:
            contact = Contact(
                member_id=member_id,
                number=number,
                first_name=first_name,
                last_name=last_name,
            )
            session.add(contact)
            session.commit()
            session.refresh(contact)

        return contact

    def get_by_id(self, id: str):
        with self.database() as session:
            contact = session.query(Contact).filter_by(id=id).all()

        return contact

    def get_by_member_id(self, member_id: str):
        with self.database() as session:
            contacts = session.query(Contact).filter_by(member_id=member_id).all()

        return contacts

    def update(self, id: str, number: str, first_name: str, last_name: str):
        with self.database() as session:
            contact = session.query(Contact).filter_by(id=id).first()

            contact.number = number
            contact.first_name = first_name
            contact.last_name = last_name

            session.commit()
            session.refresh(contact)

        return contact

    def delete(self, id: str):
        with self.database() as session:
            contact = session.query(Contact).filter_by(id=id).first()
            session.delete(contact)
            session.commit()

        return contact
