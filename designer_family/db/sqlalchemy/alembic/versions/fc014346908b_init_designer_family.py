"""init designer family

Revision ID: fc014346908b
Revises: b5c396305c25
Create Date: 2019-12-23 20:18:39.715813

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'fc014346908b'
down_revision = 'b5c396305c25'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'designers',
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=40), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    pass


def downgrade():
    op.drop_table('designers')
