"""Added created on group contacts

Revision ID: 18231c98ad52
Revises: c2016143aeff
Create Date: 2022-09-06 05:31:39.028907

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '18231c98ad52'
down_revision = 'c2016143aeff'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('group_contacts', sa.Column('created_on', postgresql.TIMESTAMP(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('group_contacts', 'created_on')
    # ### end Alembic commands ###
