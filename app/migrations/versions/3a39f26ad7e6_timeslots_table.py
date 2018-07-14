"""timeslots table

Revision ID: 3a39f26ad7e6
Revises: a81132aab2ea
Create Date: 2018-07-14 09:48:48.429687

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3a39f26ad7e6'
down_revision = 'a81132aab2ea'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('timeslot',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('index', sa.Integer(), nullable=True),
    sa.Column('time', sa.Integer(), nullable=True),
    sa.Column('date', sa.String(length=32), nullable=True),
    sa.Column('week', sa.Integer(), nullable=True),
    sa.Column('open', sa.Boolean(), nullable=True),
    sa.Column('user_id', sa.String(length=64), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('timeslot')
    # ### end Alembic commands ###
