"""empty message

Revision ID: ee161b32bad0
Revises: 2e8ec300a602
Create Date: 2018-04-08 14:16:39.641838

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ee161b32bad0'
down_revision = '2e8ec300a602'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('posts', sa.Column('html', sa.Text(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('posts', 'html')
    # ### end Alembic commands ###
