"""Updated models

Revision ID: c812f6dee8bb
Revises: 646143e802b8
Create Date: 2025-02-27 19:34:10.378205
"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# Revision identifiers, used by Alembic.
revision = 'c812f6dee8bb'
down_revision = '646143e802b8'
branch_labels = None
depends_on = None

# Define the new ENUM type
userrole_enum = postgresql.ENUM('student', 'teacher', name='userrole', create_type=False)

def upgrade():
    # Ensure the ENUM type exists before altering the column
    userrole_enum.create(op.get_bind(), checkfirst=True)

    # Manually cast values to the new ENUM type
    op.execute("ALTER TABLE subscriptions ALTER COLUMN plan TYPE userrole USING plan::userrole")
    op.execute("ALTER TABLE users ALTER COLUMN role TYPE userrole USING role::userrole")

def downgrade():
    # Reverse the ENUM type change back to VARCHAR
    op.execute("ALTER TABLE users ALTER COLUMN role TYPE VARCHAR")
    op.execute("ALTER TABLE subscriptions ALTER COLUMN plan TYPE VARCHAR")

    # Optionally, drop the ENUM type if needed
    userrole_enum.drop(op.get_bind(), checkfirst=True)
