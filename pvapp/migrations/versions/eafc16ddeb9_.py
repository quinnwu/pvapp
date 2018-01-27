"""empty message

Revision ID: eafc16ddeb9
Revises: 585ea74546fa
Create Date: 2014-03-30 02:31:33.772362

"""

# revision identifiers, used by Alembic.
revision = 'eafc16ddeb9'
down_revision = '585ea74546fa'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('project', sa.Column('secondroundscore', sa.Float(), nullable=True))
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('project', 'secondroundscore')
    ### end Alembic commands ###
