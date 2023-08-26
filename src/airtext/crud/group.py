from airtext.crud.base import DatabaseMixin
from airtext.models.group import Group


class GroupAPI(DatabaseMixin):
    def create(self, member_id: str, name: str):
        with self.database() as session:
            group = Group(
                member_id=member_id,
                name=name,
            )
            session.add(group)
            session.commit()
            session.refresh(group)

        return group

    def get_by_id(self, id: str):
        with self.database() as session:
            group = session.query(Group).filter_by(id=id).first()
        
        return group

    def get_by_member_id(self, member_id: str):
        with self.database() as session:
            groups = session.query(Group).filter_by(member_id=member_id).all()
        
        return groups
    
    def update(self, id: str, name: str):
        with self.database() as session:
            group = session.query(Group).filter_by(id=id).first()

            group.name = name

            session.commit()
            session.refresh(group)

        return group

    def delete(self, id: str):
        with self.database() as session:
            group = session.query(Group).filter_by(id=id).one()
            session.delete(group)
            session.commit()

        return group
