"""add table for hompage featured article section

Revision ID: 1fb51c9a0867
Revises: 81b6b1b74d59
Create Date: 2024-09-18 00:24:54.146866

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1fb51c9a0867'
down_revision = '81b6b1b74d59'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('featured_article',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('section_title', sa.String(length=150), nullable=True),
    sa.Column('section_body', sa.String(length=400), nullable=True),
    sa.Column('section_image_path', sa.String(length=255), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('featured_article')
    # ### end Alembic commands ###
