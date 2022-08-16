"""add unique index on proxy members

Revision ID: e3ea7fedaa2f
Revises: dda517000d94
Create Date: 2022-08-12 11:27:43.129971

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "e3ea7fedaa2f"
down_revision = "dda517000d94"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "proxy_members",
        sa.Column("id", sa.INTEGER(), nullable=False),
        sa.Column("proxy_id", sa.INTEGER(), nullable=True),
        sa.Column("member_id", sa.INTEGER(), nullable=True),
        sa.Column(
            "created_on",
            sa.TIMESTAMP(),
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["member_id"],
            ["members.id"],
        ),
        sa.ForeignKeyConstraint(
            ["proxy_id"],
            ["proxies.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("proxy_id", "member_id"),
    )
    op.drop_constraint("members_proxy_id_fkey", "members", type_="foreignkey")
    op.drop_column("members", "proxy_id")
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "members",
        sa.Column("proxy_id", sa.INTEGER(), autoincrement=False, nullable=True),
    )
    op.create_foreign_key(
        "members_proxy_id_fkey", "members", "proxies", ["proxy_id"], ["id"]
    )
    op.drop_table("proxy_members")
    # ### end Alembic commands ###
