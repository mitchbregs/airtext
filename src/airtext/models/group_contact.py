import uuid

from sqlalchemy import Column, ForeignKey, UniqueConstraint, text
from sqlalchemy.dialects.postgresql import UUID, TIMESTAMP

from airtext.models.base import BaseModel


class GroupContact(BaseModel):

    __tablename__ = "group_contacts"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    contact_id = Column(UUID(as_uuid=True), ForeignKey("contacts.id"), nullable=False)
    group_id = Column(UUID(as_uuid=True), ForeignKey("groups.id"), nullable=False)
    created_on = Column(
        TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP")
    )

    __table_args__ = (UniqueConstraint("contact_id", "group_id"),)
