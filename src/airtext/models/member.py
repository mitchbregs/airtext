from sqlalchemy import Column, ForeignKey, UniqueConstraint, text
from sqlalchemy.dialects.postgresql import ARRAY, BOOLEAN, INTEGER, TIMESTAMP, VARCHAR

from airtext.models.base import Base


class Member(Base):

    __tablename__ = "members"

    id = Column(INTEGER, primary_key=True)
    proxy_number = Column(VARCHAR(12))
    name = Column(VARCHAR(36))
    email = Column(VARCHAR(128), unique=True)
    number = Column(VARCHAR(12), nullable=False, unique=True)
    created_on = Column(
        TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP")
    )
