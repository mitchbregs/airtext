from sqlalchemy import Column, ForeignKey, UniqueConstraint, text
from sqlalchemy.dialects.postgresql import BOOLEAN, INTEGER, TIMESTAMP, VARCHAR
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


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


class Contact(Base):

    __tablename__ = "contacts"

    id = Column(INTEGER, primary_key=True)
    name = Column(VARCHAR(36))
    number = Column(VARCHAR(12), nullable=False)
    member_id = Column(INTEGER, ForeignKey("members.id"))
    created_on = Column(
        TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP")
    )

    __table_args__ = (UniqueConstraint("number", "member_id"),)


class Message(Base):

    __tablename__ = "messages"

    id = Column(INTEGER, primary_key=True)
    proxy_number = Column(VARCHAR(12), nullable=False)
    to_number = Column(VARCHAR(12))
    member_id = Column(INTEGER, ForeignKey("members.id"))
    command = Column(VARCHAR(12))
    number = Column(VARCHAR(12))
    name = Column(VARCHAR(36))
    body = Column(VARCHAR(720))
    error = Column(BOOLEAN)
    error_code = Column(VARCHAR(720))
    created_on = Column(
        TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP")
    )
