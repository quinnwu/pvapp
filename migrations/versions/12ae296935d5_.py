"""empty message

Revision ID: 12ae296935d5
Revises: 2af6e619b2f1
Create Date: 2016-01-03 19:20:57.386338

"""

# revision identifiers, used by Alembic.
revision = '12ae296935d5'
down_revision = '2af6e619b2f1'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('project', sa.Column('competitioncycle', sa.Integer(), nullable=True))
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('project', 'competitioncycle')
    ### end Alembic commands ###
