"""empty message

Revision ID: 46f83ccd8649
Revises: 2761eac32437
Create Date: 2014-02-25 00:50:19.007500

"""

# revision identifiers, used by Alembic.
revision = '46f83ccd8649'
down_revision = '2761eac32437'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('score', sa.Column('weighted', sa.Float(), nullable=True))
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('score', 'weighted')
    ### end Alembic commands ###
