"""Add user_id to requests

Revision ID: 32fc4ded79c2
Revises: afa42c441076
Create Date: 2024-11-29 23:05:30.011592

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '32fc4ded79c2'
down_revision = 'afa42c441076'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('enhancement_requests', schema=None) as batch_op:
        batch_op.add_column(sa.Column('user_id', sa.Integer(), nullable=False))
        batch_op.create_foreign_key('fk_enhancement_user_id', 'users', ['user_id'], ['id'])

    with op.batch_alter_table('pet_description_requests', schema=None) as batch_op:
        batch_op.add_column(sa.Column('user_id', sa.Integer(), nullable=False))
        batch_op.alter_column('primary_breed',
               existing_type=sa.VARCHAR(length=50),
               nullable=True)
        batch_op.alter_column('gender',
               existing_type=sa.VARCHAR(length=10),
               nullable=True)
        batch_op.alter_column('primary_color',
               existing_type=sa.VARCHAR(length=50),
               nullable=True)
        batch_op.alter_column('maturity_size',
               existing_type=sa.VARCHAR(length=50),
               nullable=True)
        batch_op.alter_column('fur_length',
               existing_type=sa.VARCHAR(length=50),
               nullable=True)
        batch_op.alter_column('vaccinated',
               existing_type=sa.VARCHAR(length=10),
               nullable=True)
        batch_op.alter_column('dewormed',
               existing_type=sa.VARCHAR(length=10),
               nullable=True)
        batch_op.alter_column('sterilized',
               existing_type=sa.VARCHAR(length=10),
               nullable=True)
        batch_op.alter_column('health',
               existing_type=sa.VARCHAR(length=50),
               nullable=True)
        batch_op.alter_column('quantity',
               existing_type=sa.INTEGER(),
               nullable=True)
        batch_op.alter_column('fee',
               existing_type=sa.FLOAT(),
               nullable=True)
        batch_op.create_foreign_key('fk_pet_description_user_id', 'users', ['user_id'], ['id'])

    with op.batch_alter_table('translation_requests', schema=None) as batch_op:
        batch_op.add_column(sa.Column('user_id', sa.Integer(), nullable=False))
        batch_op.create_foreign_key('fk_translation_user_id', 'users', ['user_id'], ['id'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('translation_requests', schema=None) as batch_op:
        batch_op.drop_constraint('fk_translation_user_id', type_='foreignkey')
        batch_op.drop_column('user_id')

    with op.batch_alter_table('pet_description_requests', schema=None) as batch_op:
        batch_op.drop_constraint('fk_pet_description_user_id', type_='foreignkey')
        batch_op.alter_column('fee',
               existing_type=sa.FLOAT(),
               nullable=False)
        batch_op.alter_column('quantity',
               existing_type=sa.INTEGER(),
               nullable=False)
        batch_op.alter_column('health',
               existing_type=sa.VARCHAR(length=50),
               nullable=False)
        batch_op.alter_column('sterilized',
               existing_type=sa.VARCHAR(length=10),
               nullable=False)
        batch_op.alter_column('dewormed',
               existing_type=sa.VARCHAR(length=10),
               nullable=False)
        batch_op.alter_column('vaccinated',
               existing_type=sa.VARCHAR(length=10),
               nullable=False)
        batch_op.alter_column('fur_length',
               existing_type=sa.VARCHAR(length=50),
               nullable=False)
        batch_op.alter_column('maturity_size',
               existing_type=sa.VARCHAR(length=50),
               nullable=False)
        batch_op.alter_column('primary_color',
               existing_type=sa.VARCHAR(length=50),
               nullable=False)
        batch_op.alter_column('gender',
               existing_type=sa.VARCHAR(length=10),
               nullable=False)
        batch_op.alter_column('primary_breed',
               existing_type=sa.VARCHAR(length=50),
               nullable=False)
        batch_op.drop_column('user_id')

    with op.batch_alter_table('enhancement_requests', schema=None) as batch_op:
        batch_op.drop_constraint('fk_enhancement_user_id', type_='foreignkey')
        batch_op.drop_column('user_id')

    # ### end Alembic commands ###
