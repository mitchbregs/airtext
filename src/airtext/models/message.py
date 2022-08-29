from sqlalchemy import Column, ForeignKey, UniqueConstraint, text
from sqlalchemy.dialects.postgresql import ARRAY, BOOLEAN, INTEGER, TIMESTAMP, VARCHAR

from airtext.models.base import Base


class Message(Base):

    __tablename__ = "messages"

    id = Column(INTEGER, primary_key=True)
    proxy_number = Column(VARCHAR(12), nullable=False)
    to_number = Column(VARCHAR(12))
    member_id = Column(INTEGER, ForeignKey("members.id"))
    command = Column(VARCHAR(12))
    numbers = Column(ARRAY(VARCHAR(12)))
    names = Column(ARRAY(VARCHAR(36)))
    groups = Column(ARRAY(VARCHAR(36)))
    body = Column(VARCHAR(720))
    error = Column(BOOLEAN)
    error_code = Column(VARCHAR(720))
    created_on = Column(
        TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP")
    )
