"""add column logo to Leadership Table

Revision ID: f415a83beb26
Revises: c54ab4422daa
Create Date: 2024-09-30 12:36:04.982723

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f415a83beb26'
down_revision = 'c54ab4422daa'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('leadership', schema=None) as batch_op:
        batch_op.add_column(sa.Column('leadership_logo', sa.String(length=255), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('leadership', schema=None) as batch_op:
        batch_op.drop_column('leadership_logo')

    # ### end Alembic commands ###