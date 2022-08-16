from sqlalchemy import Column, text
from sqlalchemy.dialects.postgresql import INTEGER, TIMESTAMP, VARCHAR

from airtext.models.mixin import DatabaseMixin, Base


class Member(Base):

    __tablename__ = "members"

    id = Column(INTEGER, primary_key=True)
    proxy_number = Column(VARCHAR(12))
    name = Column(VARCHAR(36))
    email = Column(VARCHAR(128), unique=True)
    number = Column(VARCHAR(12), nullable=False, unique=True)
    created_on = Column(TIMESTAMP, nullable=False, server_default=text("CURRENT_TIMESTAMP"))


class AirtextMembers(DatabaseMixin):

    def get_by_proxy_number(self, proxy_number: str):
        with self.session() as session:
            return session.query(Member).filter_by(proxy_number=proxy_number).one()
