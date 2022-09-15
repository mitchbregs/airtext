from sqlalchemy import Column, ForeignKey, UniqueConstraint, text
from sqlalchemy.dialects.postgresql import INTEGER, TIMESTAMP, VARCHAR
from sqlalchemy.orm import relationship

from airtext.models.base import Base


class Contact(Base):

    __tablename__ = "contacts"

    id = Column(INTEGER, primary_key=True)
    name = Column(VARCHAR(36))
    number = Column(VARCHAR(12), nullable=False)
    member_id = Column(INTEGER, ForeignKey("members.id"), nullable=False)
    created_on = Column(
        TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP")
    )

    group_contacts = relationship(
        "GroupContact", back_populates="contacts", cascade="all,delete"
    )

    __table_args__ = (
        UniqueConstraint("number", "member_id"),
        UniqueConstraint("name", "member_id"),
    )
