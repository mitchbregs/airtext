from sqlalchemy import Column, ForeignKey, UniqueConstraint, text
from sqlalchemy.dialects.postgresql import INTEGER, TIMESTAMP
from sqlalchemy.orm import relationship

from airtext.models.base import Base


class GroupContact(Base):

    __tablename__ = "group_contacts"

    id = Column(INTEGER, primary_key=True)
    contact_id = Column(INTEGER, ForeignKey("contacts.id"))
    group_id = Column(INTEGER, ForeignKey("groups.id"))
    created_on = Column(
        TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP")
    )

    contacts = relationship("Contact", back_populates="group_contacts")
    groups = relationship("Group", back_populates="group_contacts")

    __table_args__ = (UniqueConstraint("contact_id", "group_id"),)
