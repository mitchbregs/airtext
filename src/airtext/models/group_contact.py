from sqlalchemy import Column, ForeignKey, UniqueConstraint, text
from sqlalchemy.dialects.postgresql import ARRAY, BOOLEAN, INTEGER, TIMESTAMP, VARCHAR

from airtext.models.base import Base


class GroupContact(Base):

    __tablename__ = "group_contacts"

    id = Column(INTEGER, primary_key=True)
    contact_id = Column(INTEGER, ForeignKey("contacts.id"))
    group_id = Column(INTEGER, ForeignKey("groups.id"))

    __table_args__ = (UniqueConstraint("contact_id", "group_id"),)
