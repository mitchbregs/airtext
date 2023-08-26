import uuid

from sqlalchemy import Column, text
from sqlalchemy.dialects.postgresql import TIMESTAMP, VARCHAR, UUID

from airtext.models.base import BaseModel


class Member(BaseModel):

    __tablename__ = "members"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    first_name = Column(VARCHAR(36))
    last_name = Column(VARCHAR(36))
    email = Column(VARCHAR(128), nullable=False, unique=True)
    phone_number = Column(VARCHAR(12), nullable=False, unique=True)
    created_on = Column(
        TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP")
    )
