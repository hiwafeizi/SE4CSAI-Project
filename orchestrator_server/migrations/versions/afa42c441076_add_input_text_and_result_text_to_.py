"""Add input_text and result_text to PetDescriptionRequest

Revision ID: afa42c441076
Revises: 04483fe37c28
Create Date: 2024-11-29 11:39:53.816861

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'afa42c441076'
down_revision = '04483fe37c28'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('_alembic_tmp_pet_description_requests')
    with op.batch_alter_table('pet_description_requests', schema=None) as batch_op:
        batch_op.add_column(sa.Column('input_text', sa.Text(), nullable=True))
        batch_op.add_column(sa.Column('result_text', sa.Text(), nullable=True))
        batch_op.drop_column('result')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('pet_description_requests', schema=None) as batch_op:
        batch_op.add_column(sa.Column('result', sa.TEXT(), nullable=True))
        batch_op.drop_column('result_text')
        batch_op.drop_column('input_text')

    op.create_table('_alembic_tmp_pet_description_requests',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('animal_type', sa.VARCHAR(length=50), nullable=False),
    sa.Column('primary_breed', sa.VARCHAR(length=50), nullable=False),
    sa.Column('gender', sa.VARCHAR(length=10), nullable=False),
    sa.Column('primary_color', sa.VARCHAR(length=50), nullable=False),
    sa.Column('maturity_size', sa.VARCHAR(length=50), nullable=False),
    sa.Column('fur_length', sa.VARCHAR(length=50), nullable=False),
    sa.Column('vaccinated', sa.VARCHAR(length=10), nullable=False),
    sa.Column('dewormed', sa.VARCHAR(length=10), nullable=False),
    sa.Column('sterilized', sa.VARCHAR(length=10), nullable=False),
    sa.Column('health', sa.VARCHAR(length=50), nullable=False),
    sa.Column('quantity', sa.INTEGER(), nullable=False),
    sa.Column('fee', sa.FLOAT(), nullable=False),
    sa.Column('status', sa.VARCHAR(length=20), nullable=True),
    sa.Column('created_at', sa.DATETIME(), nullable=True),
    sa.Column('input_text', sa.TEXT(), nullable=False),
    sa.Column('result_text', sa.TEXT(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###
