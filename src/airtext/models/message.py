from sqlalchemy import Column, ForeignKey, UniqueConstraint, text
from sqlalchemy.dialects.postgresql import ARRAY, BOOLEAN, INTEGER, TIMESTAMP, VARCHAR
from sqlalchemy.orm import relationship

from airtext.models.base import Base


class Message(Base):

    __tablename__ = "messages"

    id = Column(INTEGER, primary_key=True)
    to_number = Column(VARCHAR(12), nullable=False)
    from_number = Column(VARCHAR(12), nullable=False)
    body_content = Column(VARCHAR(720))
    media_content = Column(VARCHAR(720))
    proxy_number = Column(VARCHAR(12), nullable=False)
    number = Column(VARCHAR(12))
    member_id = Column(INTEGER, ForeignKey("members.id"), nullable=False)
    command = Column(VARCHAR(12))
    numbers = Column(ARRAY(VARCHAR(12)))
    names = Column(ARRAY(VARCHAR(36)))
    number_names = Column(ARRAY(VARCHAR(36)))
    groups = Column(ARRAY(VARCHAR(36)))
    body = Column(VARCHAR(720))
    error = Column(BOOLEAN)
    error_code = Column(VARCHAR(720))

    created_on = Column(
        TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP")
    )
