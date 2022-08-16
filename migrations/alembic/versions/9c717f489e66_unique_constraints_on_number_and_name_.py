"""unique constraints on number and name in contacts

Revision ID: 9c717f489e66
Revises: 094538708c2d
Create Date: 2022-08-16 14:53:46.269699

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9c717f489e66'
down_revision = '094538708c2d'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('contacts_number_member_id_key', 'contacts', type_='unique')
    op.create_unique_constraint(None, 'contacts', ['name', 'number', 'member_id'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'contacts', type_='unique')
    op.create_unique_constraint('contacts_number_member_id_key', 'contacts', ['number', 'member_id'])
    # ### end Alembic commands ###
