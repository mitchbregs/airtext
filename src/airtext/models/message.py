import uuid

from sqlalchemy import Column, ForeignKey, text
from sqlalchemy.dialects.postgresql import TIMESTAMP, VARCHAR, UUID

from airtext.models.base import BaseModel


class Message(BaseModel):

    __tablename__ = "messages"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    member_id = Column(UUID(as_uuid=True), ForeignKey("members.id"), nullable=False)
    to_number = Column(VARCHAR(12), nullable=False)
    from_number = Column(VARCHAR(12), nullable=False)
    body = Column(VARCHAR(720))
    media_url = Column(VARCHAR(720))
    twilio_message_sid = Column(VARCHAR(128), nullable=False)
    twilio_uri = Column(VARCHAR(128), nullable=False)
    twilio_error_code = Column(VARCHAR(128))
    twilio_error_message = Column(VARCHAR(128))
    created_on = Column(
        TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP")
    )
