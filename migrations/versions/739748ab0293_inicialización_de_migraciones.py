"""Inicialización de migraciones

Revision ID: 739748ab0293
Revises: 
Create Date: 2024-10-19 23:42:48.421015

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '739748ab0293'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('_alembic_tmp_proyecto')
    with op.batch_alter_table('proyecto', schema=None) as batch_op:
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

    op.create_table('_alembic_tmp_proyecto',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('problema', sa.TEXT(), nullable=True),
    sa.Column('roadmap', sa.VARCHAR(length=200), nullable=True),
    sa.Column('nombre', sa.VARCHAR(length=100), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###
