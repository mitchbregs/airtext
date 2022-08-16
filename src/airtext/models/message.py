from sqlalchemy import Column, ForeignKey, UniqueConstraint, text
from sqlalchemy.dialects.postgresql import BOOLEAN, INTEGER, TIMESTAMP, VARCHAR

from airtext.models.mixin import DatabaseMixin, Base


class Message(Base):

    __tablename__ = "messages"

    id = Column(INTEGER, primary_key=True)
    proxy_number = Column(VARCHAR(12), nullable=False)
    from_number = Column(VARCHAR(12), nullable=False)
    member_id = Column(INTEGER, ForeignKey("members.id"))
    command = Column(VARCHAR(12))
    number = Column(VARCHAR(12))
    name = Column(VARCHAR(36))
    body = Column(VARCHAR(720))
    error = Column(BOOLEAN)
    error_message = Column(VARCHAR(720))
    created_on = Column(
        TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP")
    )


class AirtextMessages(DatabaseMixin):
    def add_message(
        self,
        proxy_number: str,
        from_number: str,
        member_id: int,
        command: str,
        number: str,
        name: str,
        body: str,
        error: bool,
        error_message: bool,
    ):
        with self.session() as session:
            message = Message(
                proxy_number=proxy_number,
                from_number=from_number,
                member_id=member_id,
                command=command,
                number=number,
                name=name,
                body=body,
                error=error,
                error_message=error_message,
            )
            session.add(message)
            session.commit()

        return True
