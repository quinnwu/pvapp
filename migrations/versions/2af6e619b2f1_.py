"""empty message

Revision ID: 2af6e619b2f1
Revises: 2c24bdbf26f2
Create Date: 2015-01-06 00:41:55.993339

"""

# revision identifiers, used by Alembic.
revision = '2af6e619b2f1'
down_revision = '2c24bdbf26f2'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.add_column('project', sa.Column('active', sa.Boolean, nullable=True))


def downgrade():
    op.drop_column('project','active')
