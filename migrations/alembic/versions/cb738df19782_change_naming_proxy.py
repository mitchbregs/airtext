"""change naming proxy

Revision ID: cb738df19782
Revises: 5bab4337908e
Create Date: 2022-08-12 16:01:50.418585

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'cb738df19782'
down_revision = '5bab4337908e'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('members', sa.Column('proxy_number', sa.VARCHAR(length=12), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('members', 'proxy_number')
    # ### end Alembic commands ###
