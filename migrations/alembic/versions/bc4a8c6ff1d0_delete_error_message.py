"""delete error message

Revision ID: bc4a8c6ff1d0
Revises: bd574c3ca474
Create Date: 2022-08-16 18:28:34.021888

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "bc4a8c6ff1d0"
down_revision = "bd574c3ca474"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "messages", sa.Column("error_messge", sa.VARCHAR(length=720), nullable=True)
    )
    op.drop_column("messages", "error_message")
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "messages",
        sa.Column(
            "error_message", sa.VARCHAR(length=144), autoincrement=False, nullable=True
        ),
    )
    op.drop_column("messages", "error_messge")
    # ### end Alembic commands ###
