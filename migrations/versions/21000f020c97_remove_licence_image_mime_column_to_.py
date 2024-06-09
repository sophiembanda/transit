"""Remove licence_image_mime column to Customer

Revision ID: 21000f020c97
Revises: 41ae038ebe7c
Create Date: 2024-05-17 10:43:41.981583

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '21000f020c97'
down_revision = '41ae038ebe7c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('customer', schema=None) as batch_op:
        batch_op.drop_column('licence_image_mime')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('customer', schema=None) as batch_op:
        batch_op.add_column(sa.Column('licence_image_mime', mysql.VARCHAR(length=50), nullable=False))

    # ### end Alembic commands ###
