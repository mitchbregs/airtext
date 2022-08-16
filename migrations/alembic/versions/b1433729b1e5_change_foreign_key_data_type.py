"""change foreign key data type

Revision ID: b1433729b1e5
Revises: 4ce7dd4ba5e6
Create Date: 2022-08-12 14:23:37.995483

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "b1433729b1e5"
down_revision = "4ce7dd4ba5e6"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("proxy_members")
    op.drop_table("proxies")
    op.drop_table("compaign_contacts")
    op.drop_table("campaigns")
    op.drop_table("member_contacts")
    op.add_column("contacts", sa.Column("member_id", sa.INTEGER(), nullable=True))
    op.drop_constraint("contacts_number_key", "contacts", type_="unique")
    op.create_foreign_key(None, "contacts", "members", ["member_id"], ["id"])
    op.add_column("members", sa.Column("proxy", sa.VARCHAR(length=11), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("members", "proxy")
    op.drop_constraint(None, "contacts", type_="foreignkey")
    op.create_unique_constraint("contacts_number_key", "contacts", ["number"])
    op.drop_column("contacts", "member_id")
    op.create_table(
        "proxy_members",
        sa.Column("id", sa.INTEGER(), autoincrement=True, nullable=False),
        sa.Column("proxy_id", sa.INTEGER(), autoincrement=False, nullable=True),
        sa.Column("member_id", sa.INTEGER(), autoincrement=False, nullable=True),
        sa.Column(
            "created_on",
            postgresql.TIMESTAMP(),
            server_default=sa.text("CURRENT_TIMESTAMP"),
            autoincrement=False,
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["member_id"], ["members.id"], name="proxy_members_member_id_fkey"
        ),
        sa.ForeignKeyConstraint(
            ["proxy_id"], ["proxies.id"], name="proxy_members_proxy_id_fkey"
        ),
        sa.PrimaryKeyConstraint("id", name="proxy_members_pkey"),
        sa.UniqueConstraint(
            "proxy_id", "member_id", name="proxy_members_proxy_id_member_id_key"
        ),
    )
    op.create_table(
        "member_contacts",
        sa.Column("id", sa.INTEGER(), autoincrement=True, nullable=False),
        sa.Column("member_id", sa.INTEGER(), autoincrement=False, nullable=True),
        sa.Column("contact_id", sa.INTEGER(), autoincrement=False, nullable=True),
        sa.Column(
            "created_on",
            postgresql.TIMESTAMP(),
            server_default=sa.text("CURRENT_TIMESTAMP"),
            autoincrement=False,
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["contact_id"], ["contacts.id"], name="member_contacts_contact_id_fkey"
        ),
        sa.ForeignKeyConstraint(
            ["member_id"], ["members.id"], name="member_contacts_member_id_fkey"
        ),
        sa.PrimaryKeyConstraint("id", name="member_contacts_pkey"),
    )
    op.create_table(
        "campaigns",
        sa.Column(
            "id",
            sa.INTEGER(),
            server_default=sa.text("nextval('campaigns_id_seq'::regclass)"),
            autoincrement=True,
            nullable=False,
        ),
        sa.Column("name", sa.VARCHAR(length=36), autoincrement=False, nullable=True),
        sa.Column("member_id", sa.INTEGER(), autoincrement=False, nullable=True),
        sa.Column(
            "created_on",
            postgresql.TIMESTAMP(),
            server_default=sa.text("CURRENT_TIMESTAMP"),
            autoincrement=False,
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["member_id"], ["members.id"], name="campaigns_member_id_fkey"
        ),
        sa.PrimaryKeyConstraint("id", name="campaigns_pkey"),
        postgresql_ignore_search_path=False,
    )
    op.create_table(
        "compaign_contacts",
        sa.Column("id", sa.INTEGER(), autoincrement=True, nullable=False),
        sa.Column("contact_id", sa.INTEGER(), autoincrement=False, nullable=True),
        sa.Column(
            "created_on",
            postgresql.TIMESTAMP(),
            server_default=sa.text("CURRENT_TIMESTAMP"),
            autoincrement=False,
            nullable=False,
        ),
        sa.Column("campaign_id", sa.INTEGER(), autoincrement=False, nullable=True),
        sa.ForeignKeyConstraint(
            ["campaign_id"], ["campaigns.id"], name="compaign_contacts_campaign_id_fkey"
        ),
        sa.ForeignKeyConstraint(
            ["contact_id"], ["contacts.id"], name="compaign_contacts_contact_id_fkey"
        ),
        sa.PrimaryKeyConstraint("id", name="compaign_contacts_pkey"),
    )
    op.create_table(
        "proxies",
        sa.Column("id", sa.INTEGER(), autoincrement=True, nullable=False),
        sa.Column("number", sa.VARCHAR(length=11), autoincrement=False, nullable=True),
        sa.Column(
            "created_on",
            postgresql.TIMESTAMP(),
            server_default=sa.text("CURRENT_TIMESTAMP"),
            autoincrement=False,
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id", name="proxies_pkey"),
        sa.UniqueConstraint("number", name="proxies_number_key"),
    )
    # ### end Alembic commands ###
