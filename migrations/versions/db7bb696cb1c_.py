"""empty message

Revision ID: db7bb696cb1c
Revises: 3b4b7fcf1e16
Create Date: 2019-03-29 14:58:28.185279

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'db7bb696cb1c'
down_revision = '3b4b7fcf1e16'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('booking', sa.Column('harga_bensin', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('booking', 'harga_bensin')
    # ### end Alembic commands ###