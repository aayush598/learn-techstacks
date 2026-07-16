# Alembic Migrations with FastAPI

## Table of Contents

1. [Alembic Setup](#alembic-setup)
2. [Migration Generation](#migration-generation)
3. [Autogenerate](#autogenerate)
4. [Manual Migrations](#manual-migrations)
5. [Branching](#branching)
6. [Downgrade](#downgrade)
7. [Seed Data](#seed-data)
8. [Migration Best Practices](#migration-best-practices)
9. [Handling Data Migrations](#handling-data-migrations)
10. [Multi-Environment Setup](#multi-environment-setup)
11. [Interview Questions](#interview-questions)

---

## Alembic Setup

### Installation

```bash
pip install alembic
```

### Initialize Alembic

```bash
# From project root
alembic init alembic
```

This creates:

```
alembic/
├── versions/          # Migration files
├── env.py            # Environment configuration
├── script.py.mako    # Migration template
alembic.ini           # Alembic configuration
```

### Configuration

```ini
# alembic.ini
[alembic]
script_location = alembic
prepend_sys_path = .
sqlalchemy.url = postgresql://user:pass@localhost:5432/mydb

# For async:
# sqlalchemy.url = postgresql+asyncpg://user:pass@localhost:5432/mydb
```

### env.py for Async SQLAlchemy

```python
# alembic/env.py
import asyncio
from logging.config import fileConfig

from sqlalchemy import pool
from sqlalchemy.engine import Connection
from sqlalchemy.ext.asyncio import async_engine_from_config

from alembic import context

config = context.config
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Import your models' metadata for autogenerate
from app.database import Base
from app.models import *  # noqa: F401,F403
target_metadata = Base.metadata

def run_migrations_offline() -> None:
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()

def do_run_migrations(connection: Connection) -> None:
    context.configure(connection=connection, target_metadata=target_metadata)
    with context.begin_transaction():
        context.run_migrations()

async def run_async_migrations() -> None:
    connectable = async_engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )
    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)
    await connectable.dispose()

def run_migrations_online() -> None:
    asyncio.run(run_async_migrations())

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
```

### Dynamic URL from Config

```python
# alembic/env.py
import os

def get_url():
    return os.getenv(
        "DATABASE_URL",
        "postgresql+asyncpg://user:pass@localhost:5432/mydb"
    )

config.set_main_option("sqlalchemy.url", get_url())
```

---

## Migration Generation

### Basic Commands

```bash
# Generate a migration (compares models to database)
alembic revision --autogenerate -m "add users table"

# Generate empty migration (manual)
alembic revision -m "add index on users email"

# Apply all pending migrations
alembic upgrade head

# Rollback one migration
alembic downgrade -1

# Rollback to specific revision
alembic downgrade abc123

# Show current revision
alembic current

# Show migration history
alembic history

# Show pending migrations
alembic history --indicate-head
```

### Migration File Structure

```python
# alembic/versions/abc123_add_users_table.py
"""add users table

Revision ID: abc123
Revises:
Create Date: 2024-01-15 10:30:00.000000
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers
revision: str = "abc123"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=100), nullable=False),
        sa.Column("email", sa.String(length=255), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("email"),
    )

def downgrade() -> None:
    op.drop_table("users")
```

---

## Autogenerate

### How Autogenerate Works

Alembic compares your SQLAlchemy model metadata against the actual database schema and generates migration scripts for the differences.

```bash
# Detect changes and generate migration
alembic revision --autogenerate -m "description"
```

### What Autogenerate Detects

- New tables
- Removed tables
- New columns
- Removed columns
- Changed column types
- New/removed indexes
- New/removed constraints

### What Autogenerate Does NOT Detect

- Data changes (separate data migrations needed)
- Custom SQL changes
- Renamed columns (detected as drop + add)
- Complex type changes

### Excluding Tables from Autogenerate

```python
# alembic/env.py
def include_object(object, name, type_, reflection, compare_to):
    # Exclude specific tables
    if type_ == "table" and name in ("alembic_version", "temp_table"):
        return False
    # Exclude specific schemas
    if type_ == "schema" and name in ("information_schema", "pg_catalog"):
        return False
    return True

context.configure(
    include_object=include_object,
    target_metadata=target_metadata,
)
```

### Comparing Models to a Different Database

```python
# Compare against a different database URL
def run_migrations_offline():
    url = config.get_main_option("sqlalchemy.url")
    context.configure(url=url, target_metadata=target_metadata)
    ...
```

---

## Manual Migrations

### Custom SQL in Migrations

```python
def upgrade() -> None:
    # Raw SQL
    op.execute("""
        CREATE TABLE IF NOT EXISTS audit_log (
            id SERIAL PRIMARY KEY,
            action VARCHAR(50) NOT NULL,
            created_at TIMESTAMP DEFAULT NOW()
        )
    """)

    # SQLAlchemy operations
    op.add_column(
        "users",
        sa.Column("role", sa.String(20), nullable=False, server_default="user"),
    )

    # Add index
    op.create_index(
        "ix_users_email",
        "users",
        ["email"],
        unique=True,
    )

def downgrade() -> None:
    op.drop_index("ix_users_email", table_name="users")
    op.drop_column("users", "role")
    op.execute("DROP TABLE IF EXISTS audit_log")
```

### Adding Indexes

```python
def upgrade() -> None:
    # Single column index
    op.create_index("ix_users_email", "users", ["email"])

    # Composite index
    op.create_index(
        "ix_users_status_created",
        "users",
        ["status", "created_at"],
    )

    # Partial index (PostgreSQL)
    op.execute("""
        CREATE INDEX ix_active_users
        ON users (email)
        WHERE is_active = true
    """)

    # GIN index for full-text search
    op.execute("""
        CREATE INDEX ix_users_name_gin
        ON users
        USING GIN (to_tsvector('english', name))
    """)

def downgrade() -> None:
    op.drop_index("ix_users_name_gin", table_name="users")
    op.drop_index("ix_active_users", table_name="users")
    op.drop_index("ix_users_status_created", table_name="users")
    op.drop_index("ix_users_email", table_name="users")
```

### Batch Migrations (SQLite)

```python
def upgrade() -> None:
    # SQLite doesn't support ALTER TABLE well
    # Use batch mode
    with op.batch_alter_table("users") as batch_op:
        batch_op.add_column(
            sa.Column("phone", sa.String(20), nullable=True)
        )
        batch_op.alter_column(
            "name",
            existing_type=sa.String(100),
            type_=sa.String(200),
        )

def downgrade() -> None:
    with op.batch_alter_table("users") as batch_op:
        batch_op.alter_column(
            "name",
            existing_type=sa.String(200),
            type_=sa.String(100),
        )
        batch_op.drop_column("phone")
```

---

## Branching

### Multiple Developers Working on Migrations

```bash
# Developer A
alembic revision -m "add users table"
alembic upgrade head

# Developer B (simultaneously)
alembic revision -m "add products table"
alembic upgrade head

# Now there's a merge conflict!
# Merge the branches:
alembic merge -m "merge users and products"
```

### Resolving Merge Conflicts

```python
# alembic/versions/merge_xyz.py
def upgrade() -> None:
    # Both developers added tables — just include both
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("name", sa.String(100)),
    )
    op.create_table(
        "products",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("name", sa.String(200)),
    )
```

### Preventing Branch Conflicts

- Communicate with team about migration timing
- Use sequential revision IDs (generated automatically)
- Merge main branch frequently
- Consider one migration per PR

---

## Downgrade

### Writing Downgrades

```python
def upgrade() -> None:
    op.create_table(
        "orders",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("user_id", sa.Integer(), sa.ForeignKey("users.id")),
        sa.Column("total", sa.Float()),
    )
    op.create_index("ix_orders_user_id", "orders", ["user_id"])

def downgrade() -> None:
    op.drop_index("ix_orders_user_id", table_name="orders")
    op.drop_table("orders")
```

### Common Downgrade Patterns

```python
# Add column → remove column
def upgrade():
    op.add_column("users", sa.Column("phone", sa.String(20)))

def downgrade():
    op.drop_column("users", "phone")

# Rename column → rename back
def upgrade():
    op.alter_column("users", "name", new_column_name="full_name")

def downgrade():
    op.alter_column("users", "full_name", new_column_name="name")

# Add constraint → remove constraint
def upgrade():
    op.create_unique_constraint("uq_users_email", "users", ["email"])

def downgrade():
    op.drop_constraint("uq_users_email", "users", type_="unique")
```

### Downgrade Safety

```python
# Always write downgrades — they're your safety net
# Test downgrades in development:

# Apply migration
alembic upgrade head

# Rollback
alembic downgrade -1

# Re-apply
alembic upgrade head
```

---

## Seed Data

### Seed Script

```python
# scripts/seed.py
import asyncio
from sqlmodel import Session
from app.database import engine, AsyncSessionLocal
from app.models import User, Role

async def seed():
    async with AsyncSessionLocal() as session:
        # Create roles
        roles = [
            Role(name="admin", description="Administrator"),
            Role(name="user", description="Regular user"),
            Role(name="moderator", description="Moderator"),
        ]
        session.add_all(roles)
        await session.commit()

        # Create default admin
        admin = User(
            name="Admin",
            email="admin@example.com",
            hashed_password=hash_password("admin123"),
            role_id=1,
        )
        session.add(admin)
        await session.commit()

        print("Seed data created successfully!")

if __name__ == "__main__":
    asyncio.run(seed())
```

### Migration with Seed Data

```python
# In migration file
def upgrade() -> None:
    # Create table
    op.create_table(
        "roles",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("name", sa.String(50), unique=True),
    )

    # Seed data
    op.bulk_insert(
        "roles",
        [
            {"name": "admin"},
            {"name": "user"},
            {"name": "moderator"},
        ],
    )
```

### Fixture-Based Seeding

```python
# conftest.py or scripts/
def seed_roles(session):
    roles = ["admin", "user", "moderator"]
    for role_name in roles:
        role = Role(name=role_name)
        session.add(role)
    session.commit()

def seed_test_data(session):
    seed_roles(session)
    # Add more test data
    for i in range(10):
        user = User(name=f"User {i}", email=f"user{i}@test.com")
        session.add(user)
    session.commit()
```

---

## Migration Best Practices

### 1. Always Write Downgrades

```python
# BAD: No downgrade
def upgrade():
    op.create_table("users", ...)

def downgrade():
    pass  # Can't rollback!

# GOOD: Complete downgrade
def upgrade():
    op.create_table("users", ...)

def downgrade():
    op.drop_table("users")
```

### 2. One Logical Change Per Migration

```bash
# BAD: One migration with 50 changes
alembic revision -m "add everything"

# GOOD: Separate migrations
alembic revision -m "add users table"
alembic revision -m "add items table"
alembic revision -m "add foreign keys"
```

### 3. Test Migrations Before Production

```bash
# In development:
alembic upgrade head
alembic downgrade -1
alembic upgrade head

# Verify data integrity
python scripts/verify_data.py
```

### 4. Use Descriptive Messages

```bash
# BAD
alembic revision -m "update"
alembic revision -m "fix"
alembic revision -m "changes"

# GOOD
alembic revision -m "add users table with email index"
alembic revision -m "add foreign key from orders to users"
alembic revision -m "add partial index on active users"
```

### 5. Review Generated Migrations

```python
# ALWAYS review autogenerate output before applying
alembic revision --autogenerate -m "add users"

# Check the generated file
# Verify it does what you expect
# Add any manual adjustments

# Then apply
alembic upgrade head
```

### 6. Don't Modify Applied Migrations

```bash
# Once a migration is applied to production, NEVER modify it
# Instead, create a new migration to fix issues

# BAD: Editing an existing migration
# GOOD: New migration
alembic revision -m "fix users table email length"
```

---

## Handling Data Migrations

### Data Migration Pattern

```python
def upgrade() -> None:
    # Schema change
    op.add_column("users", sa.Column("full_name", sa.String(200)))

    # Data migration
    conn = op.get_bind()
    conn.execute(
        sa.text("UPDATE users SET full_name = name WHERE full_name IS NULL")
    )

def downgrade() -> None:
    op.drop_column("users", "full_name")
```

### Complex Data Migration

```python
def upgrade() -> None:
    # Step 1: Add new column
    op.add_column("users", sa.Column("status_new", sa.String(20)))

    # Step 2: Migrate data
    conn = op.get_bind()

    # Map old boolean to new enum
    conn.execute(sa.text("""
        UPDATE users
        SET status_new = CASE
            WHEN is_active = true THEN 'active'
            WHEN is_active = false THEN 'inactive'
            ELSE 'unknown'
        END
    """))

    # Step 3: Drop old column
    op.drop_column("users", "is_active")

    # Step 4: Rename new column
    op.alter_column("users", "status_new", new_column_name="status")
```

### Reverse Data Migration

```python
def upgrade() -> None:
    op.add_column("users", sa.Column("status", sa.String(20)))
    op.add_column("users", sa.Column("is_active", sa.Boolean))

    conn = op.get_bind()
    conn.execute(sa.text("""
        UPDATE users
        SET is_active = (status = 'active')
    """))

def downgrade() -> None:
    op.drop_column("users", "is_active")
    # No need to reverse data — old column is gone
```

---

## Multi-Environment Setup

### Environment-Specific Configuration

```ini
# alembic.ini
[alembic]
script_location = alembic

[dev]
sqlalchemy.url = postgresql+asyncpg://dev:dev@localhost:5432/mydb_dev

[staging]
sqlalchemy.url = postgresql+asyncpg://staging:pass@staging-db:5432/mydb_staging

[production]
sqlalchemy.url = postgresql+asyncpg://prod:pass@prod-db:5432/mydb_prod
```

### Script for Multiple Environments

```bash
#!/bin/bash
# migrate.sh

ENV=${1:-dev}

case $ENV in
    dev)
        export DATABASE_URL="postgresql+asyncpg://dev:dev@localhost:5432/mydb_dev"
        ;;
    staging)
        export DATABASE_URL="postgresql+asyncpg://staging:pass@staging-db:5432/mydb_staging"
        ;;
    production)
        export DATABASE_URL="postgresql+asyncpg://prod:pass@prod-db:5432/mydb_prod"
        ;;
esac

alembic upgrade head
```

### CI/CD Integration

```yaml
# .github/workflows/migrate.yml
name: Database Migration

on:
  push:
    branches: [main]

jobs:
  migrate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: "3.11"
      - name: Install dependencies
        run: pip install -r requirements.txt
      - name: Run migrations
        env:
          DATABASE_URL: ${{ secrets.DATABASE_URL }}
        run: alembic upgrade head
```

---

## Interview Questions

### Q1: What is Alembic and why use it?
**Answer:** Alembic is a database migration tool for SQLAlchemy. It tracks schema changes, generates migration scripts, and applies/removes changes in a controlled manner. Essential for team development and production deployments.

### Q2: How does autogenerate work?
**Answer:** Alembic compares your SQLAlchemy model metadata against the actual database schema. Differences are automatically detected and migration scripts are generated. It detects new tables, columns, indexes, and constraints.

### Q3: What happens if a migration fails in production?
**Answer:** Use `alembic downgrade` to rollback to the previous version. Always test migrations in staging first. Have a rollback plan. Consider blue-green deployments for zero-downtime migrations.

### Q4: How do you handle data migrations?
**Answer:** Use `op.get_bind()` to execute raw SQL or SQLAlchemy queries within the migration. Always handle both the data transformation and schema change in the same migration. Test with production-like data.

### Q5: Why are downgrades important?
**Answer:** Downgrades allow you to revert changes if a migration causes issues. Without downgrades, you can't rollback and may need manual database intervention. Always write complete downgrades.

### Q6: How do you handle migration conflicts in teams?
**Answer:** Use `alembic merge` to combine branches. Communicate about migration timing. Merge main branch frequently. Consider using sequential revision strategies.

### Q7: Can you use Alembic with async SQLAlchemy?
**Answer:** Yes. Configure `env.py` to use `async_engine_from_config` and run migrations through `asyncio.run()`. The migration files themselves use sync operations, but the connection is async.

### Q8: How do you seed data with Alembic?
**Answer:** Use `op.bulk_insert()` in the migration, or create separate seed scripts that run after migrations. For complex data, use Python scripts that import your models directly.

### Q9: What is the `down_revision` in a migration?
**Answer:** `down_revision` points to the previous migration, forming a chain. This defines the order migrations are applied. It's how Alembic knows which migrations are pending.

### Q10: How do you handle multiple databases?
**Answer:** Use separate Alembic environments for each database. Configure different `env.py` files or use Alembic's multi-env support with named configurations.

---

## Summary

Alembic is essential for managing database schema changes in production FastAPI applications. Key practices: always write downgrades, test migrations before production, use descriptive messages, and never modify applied migrations.
