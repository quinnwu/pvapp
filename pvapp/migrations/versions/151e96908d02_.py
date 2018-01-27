"""empty message

Revision ID: 151e96908d02
Revises: 46f83ccd8649
Create Date: 2014-02-25 01:28:48.729593

"""

# revision identifiers, used by Alembic.
revision = '151e96908d02'
down_revision = '46f83ccd8649'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('score', sa.Column('comment', sa.String(length=2000), nullable=True))
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('score', 'comment')
    ### end Alembic commands ###
