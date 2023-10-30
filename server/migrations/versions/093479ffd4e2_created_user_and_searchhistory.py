"""created user and searchHistory

Revision ID: 093479ffd4e2
Revises: 03a641a928a9
Create Date: 2023-10-30 18:58:21.338680

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '093479ffd4e2'
down_revision = '03a641a928a9'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(), nullable=False),
    sa.Column('email', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('username')
    )
    op.create_table('search_history',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('search_date', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('search_history')
    op.drop_table('users')
    # ### end Alembic commands ###
