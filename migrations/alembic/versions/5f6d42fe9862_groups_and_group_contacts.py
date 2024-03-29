"""groups and group contacts

Revision ID: 5f6d42fe9862
Revises: 58a48011cf4b
Create Date: 2022-08-19 06:03:14.434833

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "5f6d42fe9862"
down_revision = "58a48011cf4b"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "groups",
        sa.Column("id", sa.INTEGER(), nullable=False),
        sa.Column("name", sa.VARCHAR(length=36), nullable=True),
        sa.Column("member_id", sa.INTEGER(), nullable=True),
        sa.Column(
            "created_on",
            postgresql.TIMESTAMP(),
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["member_id"],
            ["members.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("name", "member_id"),
    )
    op.create_table(
        "group_contacts",
        sa.Column("id", sa.INTEGER(), nullable=False),
        sa.Column("contact_id", sa.INTEGER(), nullable=True),
        sa.Column("group_id", sa.INTEGER(), nullable=True),
        sa.ForeignKeyConstraint(
            ["contact_id"],
            ["contacts.id"],
        ),
        sa.ForeignKeyConstraint(
            ["group_id"],
            ["groups.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.add_column(
        "messages",
        sa.Column("numbers", postgresql.ARRAY(sa.VARCHAR(length=12)), nullable=True),
    )
    op.add_column(
        "messages",
        sa.Column("names", postgresql.ARRAY(sa.VARCHAR(length=36)), nullable=True),
    )
    op.add_column(
        "messages",
        sa.Column("groups", postgresql.ARRAY(sa.VARCHAR(length=36)), nullable=True),
    )
    op.drop_column("messages", "name")
    op.drop_column("messages", "number")
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "messages",
        sa.Column("number", sa.VARCHAR(length=12), autoincrement=False, nullable=True),
    )
    op.add_column(
        "messages",
        sa.Column("name", sa.VARCHAR(length=36), autoincrement=False, nullable=True),
    )
    op.drop_column("messages", "groups")
    op.drop_column("messages", "names")
    op.drop_column("messages", "numbers")
    op.drop_table("group_contacts")
    op.drop_table("groups")
    # ### end Alembic commands ###
