"""Remove number column

Revision ID: e96d1ea78ab3
Revises: 838261f147a8
Create Date: 2022-09-08 06:23:03.423029

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e96d1ea78ab3'
down_revision = '838261f147a8'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('messages', 'number')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('messages', sa.Column('number', sa.VARCHAR(length=12), autoincrement=False, nullable=True))
    # ### end Alembic commands ###
