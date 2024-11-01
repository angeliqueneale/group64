"""Add image field to Event model

Revision ID: 37b30b0834a1
Revises: d691ae388dc2
Create Date: 2024-10-27 16:02:51.437177

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '37b30b0834a1'
down_revision = 'd691ae388dc2'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('event', schema=None) as batch_op:
        batch_op.add_column(sa.Column('image', sa.String(length=200), nullable=True))
        batch_op.alter_column('date',
               existing_type=sa.DATETIME(),
               nullable=False)
        batch_op.alter_column('status',
               existing_type=sa.VARCHAR(length=50),
               type_=sa.String(length=20),
               nullable=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('event', schema=None) as batch_op:
        batch_op.alter_column('status',
               existing_type=sa.String(length=20),
               type_=sa.VARCHAR(length=50),
               nullable=False)
        batch_op.alter_column('date',
               existing_type=sa.DATETIME(),
               nullable=True)
        batch_op.drop_column('image')

    # ### end Alembic commands ###
