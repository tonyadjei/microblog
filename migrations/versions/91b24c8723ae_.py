"""add table OurImpact

Revision ID: 91b24c8723ae
Revises: 1fb51c9a0867
Create Date: 2024-09-19 16:30:06.980749

"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "91b24c8723ae"
down_revision = "1fb51c9a0867"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "our_impact",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("section_count", sa.Integer(), nullable=True),
        sa.Column("section_title", sa.String(length=150), nullable=True),
        sa.Column("section_body", sa.String(length=400), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("our_impact")
    # ### end Alembic commands ###
