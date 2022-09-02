from airtext.crud.base import DatabaseMixin, Response
from airtext.models.group_contact import GroupContact


class GroupContactAPI(DatabaseMixin):
    def create(self, group_id: int, contact_id: int):
        with self.database() as session:
            group_contact = GroupContact(
                group_id=group_id,
                contact_id=contact_id,
            )
            session.add(group_contact)
            session.refresh(group_contact)
            session.commit()

        return Response(
            text="Successfully created group contact.",
            body=group_contact.to_dict(),
            error=False
        )

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
                return Reponse(
                    text="Group contact not found.",
                    body={},
                    error=True,
                )

            session.delete(group_contact)
            session.commit()

        return Response(
            text="Successfully removed contact from group.",
            body={},
            error=False,
        )
