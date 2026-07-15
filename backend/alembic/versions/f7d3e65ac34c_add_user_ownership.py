"""add_user_ownership

Revision ID: f7d3e65ac34c
Revises: 8f28c31ea5fd
Create Date: 2026-07-15 13:45:34.773121

"""
import uuid
from datetime import datetime, timezone
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = 'f7d3e65ac34c'
down_revision: Union[str, None] = '8f28c31ea5fd'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # 1. Add user_id as nullable columns first
    op.add_column('personas', sa.Column('user_id', sa.Uuid(), nullable=True))
    op.add_column('reports', sa.Column('user_id', sa.Uuid(), nullable=True))
    op.add_column('evaluations', sa.Column('user_id', sa.Uuid(), nullable=True))

    # 2. Backfill existing records (if any) with appropriate user ownership
    connection = op.get_bind()

    # Derived ownership for reports and evaluations from interview_sessions
    connection.execute(
        sa.text(
            "UPDATE reports "
            "SET user_id = (SELECT user_id FROM interview_sessions WHERE interview_sessions.id = reports.session_id) "
            "WHERE user_id IS NULL"
        )
    )
    connection.execute(
        sa.text(
            "UPDATE evaluations "
            "SET user_id = (SELECT user_id FROM interview_sessions WHERE interview_sessions.id = evaluations.session_id) "
            "WHERE user_id IS NULL"
        )
    )

    # For personas: check if a user exists. If not, create a system user to prevent NOT NULL FK violation.
    user_row = connection.execute(sa.text("SELECT id FROM users LIMIT 1")).fetchone()
    if not user_row:
        system_user_id = str(uuid.uuid4())
        connection.execute(
            sa.text(
                "INSERT INTO users (id, email, full_name, password_hash, created_at) "
                "VALUES (:id, :email, :full_name, :password_hash, :created_at)"
            ),
            {
                "id": system_user_id,
                "email": "system@interviewverse.ai",
                "full_name": "System Administrator",
                "password_hash": "disabled",
                "created_at": datetime.now(timezone.utc),
            }
        )
        user_id = system_user_id
    else:
        user_id = user_row[0]

    connection.execute(
        sa.text("UPDATE personas SET user_id = :user_id WHERE user_id IS NULL"),
        {"user_id": user_id}
    )

    # 3. Alter columns to NOT NULL, add foreign keys and indexes using batch_alter_table
    with op.batch_alter_table('personas', schema=None) as batch_op:
        batch_op.alter_column('user_id', existing_type=sa.Uuid(), nullable=False)
        batch_op.create_foreign_key('fk_personas_users', 'users', ['user_id'], ['id'], ondelete='CASCADE')
        batch_op.create_index('ix_personas_user_id', ['user_id'], unique=False)

    with op.batch_alter_table('reports', schema=None) as batch_op:
        batch_op.alter_column('user_id', existing_type=sa.Uuid(), nullable=False)
        batch_op.create_foreign_key('fk_reports_users', 'users', ['user_id'], ['id'], ondelete='CASCADE')
        batch_op.create_index('ix_reports_user_id', ['user_id'], unique=False)

    with op.batch_alter_table('evaluations', schema=None) as batch_op:
        batch_op.alter_column('user_id', existing_type=sa.Uuid(), nullable=False)
        batch_op.create_foreign_key('fk_evaluations_users', 'users', ['user_id'], ['id'], ondelete='CASCADE')
        batch_op.create_index('ix_evaluations_user_id', ['user_id'], unique=False)


def downgrade() -> None:
    with op.batch_alter_table('evaluations', schema=None) as batch_op:
        batch_op.drop_index('ix_evaluations_user_id')
        batch_op.drop_constraint('fk_evaluations_users', type_='foreignkey')
        batch_op.drop_column('user_id')

    with op.batch_alter_table('reports', schema=None) as batch_op:
        batch_op.drop_index('ix_reports_user_id')
        batch_op.drop_constraint('fk_reports_users', type_='foreignkey')
        batch_op.drop_column('user_id')

    with op.batch_alter_table('personas', schema=None) as batch_op:
        batch_op.drop_index('ix_personas_user_id')
        batch_op.drop_constraint('fk_personas_users', type_='foreignkey')
        batch_op.drop_column('user_id')
