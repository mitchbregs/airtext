from sqlalchemy import Column, ForeignKey, text
from sqlalchemy.dialects.postgresql import INTEGER, TIMESTAMP, VARCHAR

from airtext.models.mixin import DatabaseMixin, Base


class Contact(Base):

    __tablename__ = "contacts"

    id = Column(INTEGER, primary_key=True)
    name = Column(VARCHAR(36))
    number = Column(VARCHAR(12), nullable=False)
    member_id = Column(INTEGER, ForeignKey("members.id"))
    created_on = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
