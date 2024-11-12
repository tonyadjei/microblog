"""add table HomePageWhoWeAre

Revision ID: 81b6b1b74d59
Revises: f70af8338527
Create Date: 2024-09-17 23:21:03.755116

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '81b6b1b74d59'
down_revision = 'f70af8338527'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('home_page_who_we_are',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('section_title', sa.String(length=20), nullable=True),
    sa.Column('section_body', sa.String(length=400), nullable=True),
    sa.Column('section_image_path', sa.String(length=255), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('home_page_who_we_are')
    # ### end Alembic commands ###