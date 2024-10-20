"""Agregar campo imagen a proyecto

Revision ID: 0f99bbdafcf7
Revises: 739748ab0293
Create Date: 2024-10-19 23:52:15.607821

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0f99bbdafcf7'
down_revision = '739748ab0293'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('proyecto', schema=None) as batch_op:
        batch_op.add_column(sa.Column('imagen', sa.String(length=200), nullable=True))
        batch_op.alter_column('problema',
               existing_type=sa.TEXT(),
               nullable=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('proyecto', schema=None) as batch_op:
        batch_op.alter_column('problema',
               existing_type=sa.TEXT(),
               nullable=True)
        batch_op.drop_column('imagen')

    # ### end Alembic commands ###
