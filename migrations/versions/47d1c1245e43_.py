"""empty message

Revision ID: 47d1c1245e43
Revises:
Create Date: 2023-09-08 13:47:29.224688

"""
import sqlalchemy as sa
import sqlmodel
from alembic import op

# revision identifiers, used by Alembic.
revision = "47d1c1245e43"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "users",
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("first_name", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column("last_name", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column("email", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("uuid", sqlmodel.sql.sqltypes.GUID(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("email"),
    )
    op.create_index(op.f("ix_users_uuid"), "users", ["uuid"], unique=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f("ix_users_uuid"), table_name="users")
    op.drop_table("users")
    # ### end Alembic commands ###