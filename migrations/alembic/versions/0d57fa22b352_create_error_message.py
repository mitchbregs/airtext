"""create error message

Revision ID: 0d57fa22b352
Revises: bc4a8c6ff1d0
Create Date: 2022-08-16 18:28:51.957195

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "0d57fa22b352"
down_revision = "bc4a8c6ff1d0"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "messages", sa.Column("error_message", sa.VARCHAR(length=720), nullable=True)
    )
    op.drop_column("messages", "error_messge")
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "messages",
        sa.Column(
            "error_messge", sa.VARCHAR(length=720), autoincrement=False, nullable=True
        ),
    )
    op.drop_column("messages", "error_message")
    # ### end Alembic commands ###
