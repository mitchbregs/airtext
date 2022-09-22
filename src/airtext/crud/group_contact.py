from tokenize import group
from airtext.crud.base import DatabaseMixin
from airtext.models.contact import Contact
from airtext.models.group import Group
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

    def create_if_not_exists(self, group_id: int, contact_id: int):
        with self.database() as session:
            group_contact = (
                session.query(GroupContact)
                .filter_by(
                    group_id=group_id,
                    contact_id=contact_id
                )
                .first()
            )
            if not group_contact:
                group_contact = GroupContact(
                    group_id=group_id,
                    contact_id=contact_id,
                )
                session.add(group_contact)
                session.commit()
                session.refresh(group_contact)

        return group_contact

    def get_groups_by_contact_id(self, contact_id: int):
        with self.database() as session:
            result = (
                session.query(GroupContact, Group)
                .join(Group)
                .filter(GroupContact.contact_id == contact_id)
                .limit(5)
                .all()
            )
            return [row[1] for row in result]

    def get_by_group_id(self, group_id: int):
        with self.database() as session:
            return (
                session.query(Contact)
                .join(GroupContact)
                .filter_by(group_id=group_id)
                .all()
            )

    def get_by_group_name_and_member_id(self, group_name: str, member_id: int):
        with self.database() as session:
            return (
                session.query(Contact)
                .join(GroupContact)
                .join(Group)
                .filter(Group.name == group_name)
                .filter(Group.member_id == member_id)
                .all()
            )

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
            session.delete(group_contact)
            session.commit()

        return
