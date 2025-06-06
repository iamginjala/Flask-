"""Initial migration

Revision ID: 3a557946011e
Revises: 
Create Date: 2025-04-25 10:02:58.200026

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3a557946011e'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('movie', schema=None) as batch_op:
        batch_op.alter_column('rating',
               existing_type=sa.FLOAT(),
               nullable=True)
        batch_op.alter_column('ranking',
               existing_type=sa.INTEGER(),
               nullable=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('movie', schema=None) as batch_op:
        batch_op.alter_column('ranking',
               existing_type=sa.INTEGER(),
               nullable=False)
        batch_op.alter_column('rating',
               existing_type=sa.FLOAT(),
               nullable=False)

    # ### end Alembic commands ###
