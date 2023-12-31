"""empty message

Revision ID: 9629d49f8f0c
Revises: 7e8102696f97
Create Date: 2023-10-25 13:58:18.281427

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9629d49f8f0c'
down_revision = '7e8102696f97'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('contactus', schema=None) as batch_op:
        batch_op.add_column(sa.Column('contact_name', sa.String(length=100), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('contactus', schema=None) as batch_op:
        batch_op.drop_column('contact_name')

    # ### end Alembic commands ###
