from sqlalchemy import Column, ForeignKey, UniqueConstraint, text
from sqlalchemy.dialects.postgresql import INTEGER, TIMESTAMP, VARCHAR

from airtext.models.mixin import DatabaseMixin, Base


class Contact(Base):

    __tablename__ = "contacts"

    id = Column(INTEGER, primary_key=True)
    name = Column(VARCHAR(36))
    number = Column(VARCHAR(12), nullable=False)
    member_id = Column(INTEGER, ForeignKey("members.id"))
    created_on = Column(
        TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP")
    )

    __table_args__ = (UniqueConstraint("name", "number", "member_id"),)


class AirtextContacts(DatabaseMixin):
    def add_contact(self, name: str, number: str, member_id: int):
        with self.session() as session:
            contact = Contact(
                name=name,
                number=number,
                member_id=member_id,
            )
            session.add(contact)
            session.commit()

        return True

    def delete_contact(self, number: str, member_id: int):
        with self.session() as session:
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

    def update_contact(self, number: str, name: str, member_id: int):
        with self.session() as session:
            contact = (
                session.query(Contact)
                .filter_by(
                    number=number,
                    member_id=member_id,
                )
                .first()
            )

            if contact:
                contact.update(name=name)
                session.commit()

                return True

        return False

    def get_by_proxy_number(self, proxy_number: str):
        with self.session() as session:
            return session.query(Contact).filter_by(proxy_number=proxy_number).all()

    def get_by_name_and_member_id(self, name: str, member_id: int):
        with self.session() as session:
            return (
                session.query(Contact)
                .filter_by(
                    name=name,
                    member_id=member_id,
                )
                .first()
            )

    def get_by_number_and_member_id(self, number: str, member_id: int):
        with self.session() as session:
            return (
                session.query(Contact)
                .filter_by(
                    number=number,
                    member_id=member_id,
                )
                .first()
            )
