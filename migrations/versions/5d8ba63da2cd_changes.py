"""changes

Revision ID: 5d8ba63da2cd
Revises: 021d731ad92a
Create Date: 2023-03-11 12:19:24.833127

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5d8ba63da2cd'
down_revision = '021d731ad92a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('message',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('from_user', sa.Integer(), nullable=False),
    sa.Column('to_user', sa.Integer(), nullable=False),
    sa.Column('text', sa.String(length=10000), nullable=True),
    sa.ForeignKeyConstraint(['from_user'], ['user.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['to_user'], ['user.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('message')
    # ### end Alembic commands ###