from sqlalchemy import Column, ForeignKey, UniqueConstraint, text
from sqlalchemy.dialects.postgresql import INTEGER, TIMESTAMP, VARCHAR
from sqlalchemy.orm import relationship

from airtext.models.base import Base


class Group(Base):

    __tablename__ = "groups"

    id = Column(INTEGER, primary_key=True)
    name = Column(VARCHAR(36))
    member_id = Column(INTEGER, ForeignKey("members.id"), nullable=False)
    created_on = Column(
        TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP")
    )

    members = relationship("Member", back_populates="groups")
    group_contacts = relationship(
        "GroupContact", back_populates="groups", cascade="all,delete"
    )

    __table_args__ = (UniqueConstraint("name", "member_id"),)
