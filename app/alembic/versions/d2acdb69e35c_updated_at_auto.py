"""updated_at_auto

Revision ID: d2acdb69e35c
Revises: cbf81942aff3
Create Date: 2026-08-30 14:20:59.369699

"""

from collections.abc import Sequence

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "d2acdb69e35c"
down_revision: str | Sequence[str] | None = "cbf81942aff3"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.execute(
        """
        CREATE OR REPLACE FUNCTION set_updated_at()
        RETURNS TRIGGER AS $$
        BEGIN
            NEW.updated_at = NOW();
            RETURN NEW;
        END;
        $$ LANGUAGE plpgsql;
        """
    )

    op.execute(
        """
        CREATE TRIGGER set_reader_updated_at
        BEFORE UPDATE ON reader
        FOR EACH ROW
        EXECUTE FUNCTION set_updated_at();
        """
    )

    op.execute(
        """
        CREATE TRIGGER set_book_updated_at
        BEFORE UPDATE ON book
        FOR EACH ROW
        EXECUTE FUNCTION set_updated_at();
        """
    )


def downgrade() -> None:
    op.execute("DROP TRIGGER IF EXISTS set_book_updated_at ON book;")
    op.execute("DROP TRIGGER IF EXISTS set_reader_updated_at ON reader;")
    op.execute("DROP FUNCTION IF EXISTS set_updated_at();")
