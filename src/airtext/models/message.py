from sqlalchemy import Column, ForeignKey, UniqueConstraint, text
from sqlalchemy.dialects.postgresql import BOOLEAN, INTEGER, JSON, TIMESTAMP, VARCHAR
from sqlalchemy.orm import relationship

from airtext.models.base import Base


class Message(Base):

    __tablename__ = "messages"

    id = Column(INTEGER, primary_key=True)
    to_number = Column(VARCHAR(12), nullable=False)
    from_number = Column(VARCHAR(12), nullable=False)
    body = Column(VARCHAR(720))
    media_url = Column(VARCHAR(720))
    proxy_number = Column(VARCHAR(12), nullable=False)
    member_id = Column(INTEGER, ForeignKey("members.id"), nullable=False)
    command = Column(VARCHAR(12))
    contacts = Column(JSON)
    groups = Column(JSON)
    body_content = Column(VARCHAR(720))
    error = Column(BOOLEAN)
    error_message = Column(VARCHAR(720))

    twilio_uri = Column(VARCHAR(128), nullable=False)
    twilio_error_code = Column(VARCHAR(128))
    twilio_error_message = Column(VARCHAR(128))

    created_on = Column(
        TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP")
    )
