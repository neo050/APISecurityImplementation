"""Increase password_hash length

Revision ID: 7481dbf3bfd8
Revises: a6210b92a62b
Create Date: 2024-08-31 17:01:28.540081

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7481dbf3bfd8'
down_revision = 'a6210b92a62b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.alter_column('password_hash',
               existing_type=sa.VARCHAR(length=128),
               type_=sa.String(length=255),
               existing_nullable=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.alter_column('password_hash',
               existing_type=sa.String(length=255),
               type_=sa.VARCHAR(length=128),
               existing_nullable=False)

    # ### end Alembic commands ###
