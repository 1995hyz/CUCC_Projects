"""users table

Revision ID: a81132aab2ea
Revises: 301ac5823a60
Create Date: 2018-07-10 21:04:49.877967

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a81132aab2ea'
down_revision = '301ac5823a60'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('privilege', sa.Boolean(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'privilege')
    # ### end Alembic commands ###