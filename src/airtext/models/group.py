from sqlalchemy import Column, ForeignKey, UniqueConstraint, text
from sqlalchemy.dialects.postgresql import ARRAY, BOOLEAN, INTEGER, TIMESTAMP, VARCHAR

from airtext.models.base import Base


class Group(Base):

    __tablename__ = "groups"

    id = Column(INTEGER, primary_key=True)
    name = Column(VARCHAR(36))
    member_id = Column(INTEGER, ForeignKey("members.id"))
    created_on = Column(
        TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP")
    )

    __table_args__ = (UniqueConstraint("name", "member_id"),)
