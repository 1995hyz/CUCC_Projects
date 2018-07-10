"""users table

Revision ID: 301ac5823a60
Revises: dab09fd0bd02
Create Date: 2018-07-09 20:37:20.489815

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '301ac5823a60'
down_revision = 'dab09fd0bd02'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('first_name', sa.String(length=64), nullable=True))
    op.add_column('user', sa.Column('last_name', sa.String(length=64), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'last_name')
    op.drop_column('user', 'first_name')
    # ### end Alembic commands ###
