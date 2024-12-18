"""add Carousel Table

Revision ID: 9a704b1a1fb6
Revises: 91b24c8723ae
Create Date: 2024-09-23 17:11:00.468497

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9a704b1a1fb6'
down_revision = '91b24c8723ae'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('carousel',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('section_title', sa.String(length=200), nullable=True),
    sa.Column('section_image_path', sa.String(length=255), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('carousel')
    # ### end Alembic commands ###
