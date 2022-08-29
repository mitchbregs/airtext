from airtext.crud.base import ExternalConnectionsMixin
from airtext.models.contact import Contact
from airtext.models.group import Group
from airtext.models.group_contact import GroupContact


class GroupContactAPI(ExternalConnectionsMixin):
    def get_by_name_and_member_id(self, name: str, member_id: int):
        with self.database() as session:
            results = (
                session.query(GroupContact, Group, Contact)
                .join(Group)
                .join(Contact)
                .filter(Group.name == name)
                .filter(Group.member_id == member_id)
                .filter_by(proxy_number=proxy_number)
                .all()
            )

        import ipdb

        ipdb.set_trace()
        return []
