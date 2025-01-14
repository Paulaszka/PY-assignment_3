"""Initial migration

Revision ID: feb90dba6c32
Revises: 
Create Date: 2025-01-14 19:19:13.782721

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'feb90dba6c32'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('numbers',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('feature1', sa.Float(), nullable=False),
    sa.Column('feature2', sa.Float(), nullable=False),
    sa.Column('category', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('numbers')
    # ### end Alembic commands ###
