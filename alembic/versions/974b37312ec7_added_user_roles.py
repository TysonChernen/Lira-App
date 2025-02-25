"""Added user roles

Revision ID: 974b37312ec7
Revises: ed407b0d1be1
Create Date: 2025-02-25 11:53:54.831382

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = '974b37312ec7'
down_revision: Union[str, None] = 'ed407b0d1be1'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

# Define ENUM type for user roles
user_role_enum = sa.Enum('student', 'teacher', name='userrole')

def upgrade() -> None:
    # First, create the ENUM type
    user_role_enum.create(op.get_bind())

    # Then, modify the users table
    op.add_column('users', sa.Column('hashed_password', sa.String(), nullable=True))
    op.add_column('users', sa.Column('role', user_role_enum, nullable=True))
    op.drop_column('users', 'password')

def downgrade() -> None:
    # Remove the role column first
    op.drop_column('users', 'role')

    # Drop the ENUM type after removing the column
    user_role_enum.drop(op.get_bind())

    # Restore the previous password column
    op.add_column('users', sa.Column('password', sa.VARCHAR(), autoincrement=False, nullable=True))
    op.drop_column('users', 'hashed_password')

