"""add post for user_id

Revision ID: 3c46e4a028a6
Revises: 9c7ef09cf19c
Create Date: 2018-04-07 16:06:30.855782

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '3c46e4a028a6'
down_revision = '9c7ef09cf19c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('posts', sa.Column('user_id', sa.Integer(), nullable=True))
    op.drop_constraint('posts_ibfk_1', 'posts', type_='foreignkey')
    op.create_foreign_key(None, 'posts', 'users', ['user_id'], ['id'])
    op.drop_column('posts', 'user')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('posts', sa.Column('user', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True))
    op.drop_constraint(None, 'posts', type_='foreignkey')
    op.create_foreign_key('posts_ibfk_1', 'posts', 'users', ['user'], ['id'])
    op.drop_column('posts', 'user_id')
    # ### end Alembic commands ###
