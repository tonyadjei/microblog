"""add timestamp fields to some models

Revision ID: 9f2add8f9058
Revises: 2b30b251d55a
Create Date: 2024-10-11 17:22:58.754568

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9f2add8f9058'
down_revision = '2b30b251d55a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('events', schema=None) as batch_op:
        batch_op.add_column(sa.Column('created_date', sa.DateTime(), nullable=True))
        batch_op.add_column(sa.Column('last_modified', sa.DateTime(), nullable=True))
        batch_op.create_index(batch_op.f('ix_events_created_date'), ['created_date'], unique=False)
        batch_op.create_index(batch_op.f('ix_events_last_modified'), ['last_modified'], unique=False)

    with op.batch_alter_table('industry_updates', schema=None) as batch_op:
        batch_op.add_column(sa.Column('created_date', sa.DateTime(), nullable=True))
        batch_op.add_column(sa.Column('last_modified', sa.DateTime(), nullable=True))
        batch_op.create_index(batch_op.f('ix_industry_updates_created_date'), ['created_date'], unique=False)
        batch_op.create_index(batch_op.f('ix_industry_updates_last_modified'), ['last_modified'], unique=False)

    with op.batch_alter_table('latest_news', schema=None) as batch_op:
        batch_op.add_column(sa.Column('created_date', sa.DateTime(), nullable=True))
        batch_op.add_column(sa.Column('last_modified', sa.DateTime(), nullable=True))
        batch_op.create_index(batch_op.f('ix_latest_news_created_date'), ['created_date'], unique=False)
        batch_op.create_index(batch_op.f('ix_latest_news_last_modified'), ['last_modified'], unique=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('latest_news', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_latest_news_last_modified'))
        batch_op.drop_index(batch_op.f('ix_latest_news_created_date'))
        batch_op.drop_column('last_modified')
        batch_op.drop_column('created_date')

    with op.batch_alter_table('industry_updates', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_industry_updates_last_modified'))
        batch_op.drop_index(batch_op.f('ix_industry_updates_created_date'))
        batch_op.drop_column('last_modified')
        batch_op.drop_column('created_date')

    with op.batch_alter_table('events', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_events_last_modified'))
        batch_op.drop_index(batch_op.f('ix_events_created_date'))
        batch_op.drop_column('last_modified')
        batch_op.drop_column('created_date')

    # ### end Alembic commands ###
