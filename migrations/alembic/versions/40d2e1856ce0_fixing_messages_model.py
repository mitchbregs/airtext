"""fixing messages model

Revision ID: 40d2e1856ce0
Revises: a651022e0435
Create Date: 2022-09-13 03:12:36.816562

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '40d2e1856ce0'
down_revision = 'a651022e0435'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('messages', sa.Column('contacts', postgresql.ARRAY(sa.VARCHAR(length=36)), nullable=True))
    op.add_column('messages', sa.Column('error_message', sa.VARCHAR(length=720), nullable=True))
    op.drop_column('messages', 'number_names')
    op.drop_column('messages', 'names')
    op.drop_column('messages', 'numbers')
    op.drop_column('messages', 'error_code')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('messages', sa.Column('error_code', sa.VARCHAR(length=720), autoincrement=False, nullable=True))
    op.add_column('messages', sa.Column('numbers', postgresql.ARRAY(sa.VARCHAR(length=12)), autoincrement=False, nullable=True))
    op.add_column('messages', sa.Column('names', postgresql.ARRAY(sa.VARCHAR(length=36)), autoincrement=False, nullable=True))
    op.add_column('messages', sa.Column('number_names', postgresql.ARRAY(sa.VARCHAR(length=36)), autoincrement=False, nullable=True))
    op.drop_column('messages', 'error_message')
    op.drop_column('messages', 'contacts')
    # ### end Alembic commands ###