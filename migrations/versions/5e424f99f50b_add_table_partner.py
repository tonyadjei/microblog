"""add table Partner

Revision ID: 5e424f99f50b
Revises: f415a83beb26
Create Date: 2024-09-30 12:37:46.839808

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5e424f99f50b'
down_revision = 'f415a83beb26'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('partner',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('partner_name', sa.String(length=150), nullable=True),
    sa.Column('partner_description', sa.String(length=200), nullable=True),
    sa.Column('partner_logo', sa.String(length=255), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('partner')
    # ### end Alembic commands ###
