"""Adding Relationship to Refresh Token

Revision ID: a74bea33c200
Revises: e476c0ee1703
Create Date: 2024-11-21 11:55:08.963236

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a74bea33c200'
down_revision: Union[str, None] = 'e476c0ee1703'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('refresh_tokens_user_id_fkey', 'refresh_tokens', type_='foreignkey')
    op.create_foreign_key(None, 'refresh_tokens', 'users', ['user_id'], ['id'], ondelete='CASCADE')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'refresh_tokens', type_='foreignkey')
    op.create_foreign_key('refresh_tokens_user_id_fkey', 'refresh_tokens', 'users', ['user_id'], ['id'])
    # ### end Alembic commands ###