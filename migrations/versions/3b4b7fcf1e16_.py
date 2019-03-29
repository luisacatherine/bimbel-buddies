"""empty message

Revision ID: 3b4b7fcf1e16
Revises: b411b32b2126
Create Date: 2019-03-29 14:39:30.329576

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '3b4b7fcf1e16'
down_revision = 'b411b32b2126'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('booking', sa.Column('saldo_tentor', sa.Integer(), nullable=True))
    op.drop_column('booking', 'saldo_mentor')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('booking', sa.Column('saldo_mentor', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True))
    op.drop_column('booking', 'saldo_tentor')
    # ### end Alembic commands ###
