"""empty message

Revision ID: b7f3d38ec501
Revises: db7bb696cb1c
Create Date: 2019-03-31 14:29:00.115103

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b7f3d38ec501'
down_revision = 'db7bb696cb1c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('reviews', sa.Column('id_booking', sa.Integer(), nullable=True))
    op.create_unique_constraint(None, 'reviews', ['id_booking'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'reviews', type_='unique')
    op.drop_column('reviews', 'id_booking')
    # ### end Alembic commands ###
