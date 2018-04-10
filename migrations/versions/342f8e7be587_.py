"""empty message

Revision ID: 342f8e7be587
Revises: 4af567e4883c
Create Date: 2018-04-10 11:42:37.213083

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '342f8e7be587'
down_revision = '4af567e4883c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('comments',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('body', sa.Text(), nullable=True),
    sa.Column('html', sa.Text(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('post_id', sa.Integer(), nullable=True),
    sa.Column('time', sa.DateTime(), nullable=True),
    sa.Column('disable', sa.Boolean(), nullable=True),
    sa.ForeignKeyConstraint(['post_id'], ['posts.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_comments_time'), 'comments', ['time'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_comments_time'), table_name='comments')
    op.drop_table('comments')
    # ### end Alembic commands ###