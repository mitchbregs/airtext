"""Update message model

Revision ID: bc80a9ff7371
Revises: efccc07b6beb
Create Date: 2022-08-30 04:36:13.688170

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'bc80a9ff7371'
down_revision = 'efccc07b6beb'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('t_e')
    op.add_column('messages', sa.Column('from_number', sa.VARCHAR(length=12), nullable=False))
    op.add_column('messages', sa.Column('body_content', sa.VARCHAR(length=720), nullable=True))
    op.add_column('messages', sa.Column('media_content', sa.VARCHAR(length=720), nullable=True))
    op.add_column('messages', sa.Column('number', sa.VARCHAR(length=12), nullable=True))
    op.alter_column('messages', 'to_number',
               existing_type=sa.VARCHAR(length=12),
               nullable=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('messages', 'to_number',
               existing_type=sa.VARCHAR(length=12),
               nullable=True)
    op.drop_column('messages', 'number')
    op.drop_column('messages', 'media_content')
    op.drop_column('messages', 'body_content')
    op.drop_column('messages', 'from_number')
    op.create_table('t_e',
    sa.Column('docs', sa.TEXT(), autoincrement=False, nullable=True)
    )
    # ### end Alembic commands ###
