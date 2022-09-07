from airtext.crud.base import DatabaseMixin
from airtext.models.group import Group
from airtext.models.member import Member


class GroupAPI(DatabaseMixin):
    def create(self, name: str, member_id: int):
        with self.database() as session:
            group = Group(
                name=name,
                member_id=member_id,
            )
            session.add(group)
            session.commit()
            session.refresh(group)

        return group

    def get_by_member_id(self, member_id: int):
        with self.database() as session:
            return (
                session.query(Group)
                .filter_by(member_id=member_id)
                .one()
            )

    def get_by_proxy_number(self, proxy_number: str):
        with self.database() as session:
            return (
                session.query(Group)
                .join(Member)
                .filter_by(proxy_number=proxy_number)
                .all()
            )

    def delete(self, group_id: int):
        with self.database() as session:
            group = (
                session.query(Group)
                .filter_by(group_id=group_id)
                .one()
            )
            session.delete(group)
            session.commit()

        return group
