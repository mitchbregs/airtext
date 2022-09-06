from airtext.crud.base import DatabaseMixin
from airtext.models.group_contact import GroupContact


class GroupContactAPI(DatabaseMixin):
    def create(self, group_id: int, contact_id: int):
        with self.database() as session:
            group_contact = GroupContact(
                group_id=group_id,
                contact_id=contact_id,
            )
            session.add(group_contact)
            session.commit()
            session.refresh(group_contact)

        return group_contact

    def get_by_group_id(self, group_id: int):
        with self.database() as session:
            return session.query(GroupContact).filter_by(group_id=group_id).all()

    def delete(self, group_id: int, contact_id: int):
        with self.database() as session:
            group_contact = (
                session.query(GroupContact)
                .filter_by(
                    group_id=group_id,
                    contact_id=contact_id,
                )
                .first()
            )

            if not group_contact:
                return False

            session.delete(group_contact)
            session.commit()

        return True
