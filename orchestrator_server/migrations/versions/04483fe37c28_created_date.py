"""created date

Revision ID: 04483fe37c28
Revises: 29b72388e71f
Create Date: 2024-11-29 10:29:16.743211

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '04483fe37c28'
down_revision = '29b72388e71f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('enhancement_requests', schema=None) as batch_op:
        batch_op.add_column(sa.Column('created_at', sa.DateTime(), nullable=True))

    with op.batch_alter_table('pet_description_requests', schema=None) as batch_op:
        batch_op.add_column(sa.Column('created_at', sa.DateTime(), nullable=True))

    with op.batch_alter_table('translation_requests', schema=None) as batch_op:
        batch_op.add_column(sa.Column('created_at', sa.DateTime(), nullable=True))

    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('created_at', sa.DateTime(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_column('created_at')

    with op.batch_alter_table('translation_requests', schema=None) as batch_op:
        batch_op.drop_column('created_at')

    with op.batch_alter_table('pet_description_requests', schema=None) as batch_op:
        batch_op.drop_column('created_at')

    with op.batch_alter_table('enhancement_requests', schema=None) as batch_op:
        batch_op.drop_column('created_at')

    # ### end Alembic commands ###
