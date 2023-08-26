import uuid

from sqlalchemy import Column, ForeignKey, text
from sqlalchemy.dialects.postgresql import TIMESTAMP, VARCHAR, UUID

from airtext.models.base import BaseModel


class Contact(BaseModel):

    __tablename__ = "contacts"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    member_id = Column(UUID(as_uuid=True), ForeignKey("members.id"), nullable=False)
    number = Column(VARCHAR(12), nullable=False)
    first_name = Column(VARCHAR(36))
    last_name = Column(VARCHAR(36))
    created_on = Column(
        TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP")
    )
