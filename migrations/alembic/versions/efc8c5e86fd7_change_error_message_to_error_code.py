"""change error_message to error_code

Revision ID: efc8c5e86fd7
Revises: d3ab0454dbb8
Create Date: 2022-08-18 03:39:44.042695

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "efc8c5e86fd7"
down_revision = "d3ab0454dbb8"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "messages", sa.Column("error_code", sa.VARCHAR(length=720), nullable=True)
    )
    op.drop_column("messages", "error_message")
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "messages",
        sa.Column(
            "error_message", sa.VARCHAR(length=720), autoincrement=False, nullable=True
        ),
    )
    op.drop_column("messages", "error_code")
    # ### end Alembic commands ###
