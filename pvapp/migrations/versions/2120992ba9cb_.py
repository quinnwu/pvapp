"""empty message

Revision ID: 2120992ba9cb
Revises: 5d0a5822582
Create Date: 2014-03-01 17:48:01.855038

"""

# revision identifiers, used by Alembic.
revision = '2120992ba9cb'
down_revision = '5d0a5822582'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('project', sa.Column('firstround', sa.Float(), nullable=True))
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('project', 'firstround')
    ### end Alembic commands ###