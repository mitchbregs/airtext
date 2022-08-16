"""deleted test table

Revision ID: 2276946b4396
Revises: 3a40cadaf40f
Create Date: 2022-08-13 12:33:14.431432

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "2276946b4396"
down_revision = "3a40cadaf40f"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("tests")
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "tests",
        sa.Column("id", sa.INTEGER(), autoincrement=True, nullable=False),
        sa.PrimaryKeyConstraint("id", name="tests_pkey"),
    )
    # ### end Alembic commands ###
