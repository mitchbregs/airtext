"""change naming

Revision ID: 5bab4337908e
Revises: f9d1f5e96111
Create Date: 2022-08-12 16:01:36.879138

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5bab4337908e'
down_revision = 'f9d1f5e96111'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('contacts', sa.Column('number', sa.VARCHAR(length=12), nullable=True))
    op.drop_column('contacts', 'phone_number')
    op.add_column('members', sa.Column('number', sa.VARCHAR(length=12), nullable=True))
    op.drop_constraint('members_phone_number_key', 'members', type_='unique')
    op.create_unique_constraint(None, 'members', ['number'])
    op.drop_column('members', 'phone_number')
    op.drop_column('members', 'proxy_number')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('members', sa.Column('proxy_number', sa.VARCHAR(length=12), autoincrement=False, nullable=True))
    op.add_column('members', sa.Column('phone_number', sa.VARCHAR(length=12), autoincrement=False, nullable=True))
    op.drop_constraint(None, 'members', type_='unique')
    op.create_unique_constraint('members_phone_number_key', 'members', ['phone_number'])
    op.drop_column('members', 'number')
    op.add_column('contacts', sa.Column('phone_number', sa.VARCHAR(length=12), autoincrement=False, nullable=True))
    op.drop_column('contacts', 'number')
    # ### end Alembic commands ###
