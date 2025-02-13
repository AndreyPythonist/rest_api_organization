"""initial

Revision ID: 9b3654e63451
Revises: 
Create Date: 2025-02-12 22:39:18.841654

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy import text
from pathlib import Path


# revision identifiers, used by Alembic.
revision: str = '9b3654e63451'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('activity',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('parent_id', sa.UUID(), nullable=True),
    sa.Column('value', sa.VARCHAR(length=255), nullable=False),
    sa.ForeignKeyConstraint(['parent_id'], ['activity.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('building',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('address', sa.VARCHAR(length=255), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('coordinates',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('building_id', sa.UUID(), nullable=False),
    sa.Column('latitude', sa.DECIMAL(precision=8, scale=6), nullable=False),
    sa.Column('longitude', sa.DECIMAL(precision=9, scale=6), nullable=False),
    sa.ForeignKeyConstraint(['building_id'], ['building.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('building_id')
    )
    op.create_table('organization',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('building_id', sa.UUID(), nullable=False),
    sa.Column('name', sa.VARCHAR(length=255), nullable=False),
    sa.ForeignKeyConstraint(['building_id'], ['building.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('activity_organization',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('organization_id', sa.UUID(), nullable=True),
    sa.Column('activity_id', sa.UUID(), nullable=True),
    sa.ForeignKeyConstraint(['activity_id'], ['activity.id'], ),
    sa.ForeignKeyConstraint(['organization_id'], ['organization.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('phone_number',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('organization_id', sa.UUID(), nullable=False),
    sa.Column('number', sa.VARCHAR(length=30), nullable=False),
    sa.ForeignKeyConstraint(['organization_id'], ['organization.id'], ),
    sa.PrimaryKeyConstraint('id')
    )

    dump_path = Path(__file__).parent.parent.absolute() / 'dumps' / 'model.dump'

    with open(dump_path, 'r') as sql_reader:
        op.execute(text(sql_reader.read()))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('phone_number')
    op.drop_table('activity_organization')
    op.drop_table('organization')
    op.drop_table('coordinates')
    op.drop_table('building')
    op.drop_table('activity')
    # ### end Alembic commands ###
