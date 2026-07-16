# CI Testing

## Table of Contents

1. [Testing in CI/CD Pipelines](#1-cicd)
2. [Parallel Testing](#2-parallel)
3. [Test Coverage](#3-coverage)
4. [Test Reporting](#4-reporting)
5. [Database Migrations in Tests](#5-migrations)
6. [Docker-Based Testing](#6-docker)
7. [Test Environment Management](#7-environment)
8. [GitHub Actions Configuration](#8-github-actions)
9. [GitLab CI Configuration](#9-gitlab-ci)
10. [Test Performance Optimization](#10-optimization)
11. [Flaky Test Management](#11-flaky)
12. [Security Testing in CI](#12-security)
13. [Best Practices](#13-best-practices)

---

## 1. Testing in CI/CD Pipelines <a name="1-cicd"></a>

### Pipeline Structure

```yaml
# .github/workflows/ci.yml
name: CI Pipeline

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.12"
      - run: pip install ruff mypy
      - run: ruff check .
      - run: mypy app/

  test-unit:
    runs-on: ubuntu-latest
    needs: lint
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.12"
          cache: pip
      - run: pip install -r requirements.txt -r requirements-test.txt
      - run: pytest -m unit -v --cov=app --cov-report=xml

  test-integration:
    runs-on: ubuntu-latest
    needs: lint
    services:
      postgres:
        image: postgres:16
        env:
          POSTGRES_USER: test
          POSTGRES_PASSWORD: test
          POSTGRES_DB: test_db
        ports:
          - 5432:5432
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
      redis:
        image: redis:7
        ports:
          - 6379:6379
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.12"
          cache: pip
      - run: pip install -r requirements.txt -r requirements-test.txt
      - run: alembic upgrade head
        env:
          DATABASE_URL: postgresql://test:test@localhost:5432/test_db
      - run: pytest -m integration -v --cov=app --cov-report=xml
        env:
          DATABASE_URL: postgresql://test:test@localhost:5432/test_db
          REDIS_URL: redis://localhost:6379

  coverage:
    runs-on: ubuntu-latest
    needs: [test-unit, test-integration]
    steps:
      - uses: actions/checkout@v4
      - uses: codecov/codecov-action@v4
        with:
          file: ./coverage.xml
          fail_ci_if_error: true
```

### FastAPI CI Pipeline Template

```yaml
# Complete CI/CD pipeline for FastAPI
name: FastAPI CI/CD

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

env:
  PYTHON_VERSION: "3.12"
  POSTGRES_USER: test
  POSTGRES_PASSWORD: test
  POSTGRES_DB: test_db

jobs:
  # Stage 1: Code Quality
  quality:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: ${{ env.PYTHON_VERSION }}
      - run: pip install ruff mypy bandit
      - run: ruff check . --output-format=github
      - run: mypy app/ --strict
      - run: bandit -r app/ -ll

  # Stage 2: Unit Tests
  unit-tests:
    runs-on: ubuntu-latest
    needs: quality
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: ${{ env.PYTHON_VERSION }}
          cache: pip
      - run: pip install -e ".[test]"
      - run: pytest tests/unit/ -v --tb=short

  # Stage 3: Integration Tests
  integration-tests:
    runs-on: ubuntu-latest
    needs: quality
    services:
      postgres:
        image: postgres:16
        env:
          POSTGRES_USER: ${{ env.POSTGRES_USER }}
          POSTGRES_PASSWORD: ${{ env.POSTGRES_PASSWORD }}
          POSTGRES_DB: ${{ env.POSTGRES_DB }}
        ports:
          - 5432:5432
        options: --health-cmd pg_isready --health-interval 10s --health-timeout 5s --health-retries 5
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: ${{ env.PYTHON_VERSION }}
          cache: pip
      - run: pip install -e ".[test]"
      - run: alembic upgrade head
      - run: pytest tests/integration/ -v --tb=short
        env:
          DATABASE_URL: postgresql://${{ env.POSTGRES_USER }}:${{ env.POSTGRES_PASSWORD }}@localhost:5432/${{ env.POSTGRES_DB }}

  # Stage 4: Coverage
  coverage:
    runs-on: ubuntu-latest
    needs: [unit-tests, integration-tests]
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: ${{ env.PYTHON_VERSION }}
          cache: pip
      - run: pip install -e ".[test]"
      - run: pytest --cov=app --cov-report=xml --cov-report=html
      - uses: codecov/codecov-action@v4
        with:
          file: ./coverage.xml
      - uses: actions/upload-artifact@v4
        with:
          name: coverage-report
          path: htmlcov/

  # Stage 5: Security Scan
  security:
    runs-on: ubuntu-latest
    needs: quality
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: ${{ env.PYTHON_VERSION }}
      - run: pip install safety bandit semgrep
      - run: safety check -r requirements.txt
      - run: bandit -r app/ -f json -o bandit-report.json || true
      - run: semgrep --config=auto app/
```

---

## 2. Parallel Testing <a name="2-parallel"></a>

### pytest-xdist

```bash
pip install pytest-xdist
```

```bash
# Auto-detect CPU count
pytest -n auto

# Specify number of workers
pytest -n 4

# With coverage (requires coverage configuration)
pytest -n auto --cov=app --cov-report=xml

# Distributed testing across multiple machines
pytest -d --rsyncdir=app tests/
```

### Parallel Test Configuration

```toml
# pyproject.toml
[tool.pytest.ini_options]
addopts = [
    "-n", "auto",           # Parallel by default
    "--dist", "loadgroup",  # Balance load across workers
]

[tool.coverage.run]
# Coverage for parallel testing
parallel = true
source = ["app"]

[tool.coverage.paths]
source = ["app", "**/site-packages/app"]
```

### Grouping Tests for Parallel Safety

```python
import pytest

@pytest.mark.dist(group=1)
def test_database_write():
    """All DB writes go to same group to avoid conflicts."""
    pass

@pytest.mark.dist(group=2)
def test_database_read():
    """Reads can run in parallel."""
    pass

# Or use pytest markers
@pytest.mark.parallel
def test_independent():
    """This test has no side effects."""
    pass
```

### Handling Shared Resources

```python
import pytest
import tempfile
import os

@pytest.fixture
def temp_file():
    """Each parallel worker gets its own temp file."""
    fd, path = tempfile.mkstemp()
    yield path
    os.close(fd)
    os.unlink(path)

def test_with_temp_file(temp_file):
    with open(temp_file, "w") as f:
        f.write("test data")
    with open(temp_file, "r") as f:
        assert f.read() == "test data"

# Database isolation for parallel tests
@pytest.fixture
def isolated_db():
    """Each worker gets a unique database."""
    import uuid
    db_name = f"test_{uuid.uuid4().hex[:8]}"
    engine = create_engine(f"sqlite:///{db_name}.db")
    Base.metadata.create_all(bind=engine)
    yield engine
    Base.metadata.drop_all(bind=engine)
    os.remove(f"{db_name}.db")
```

---

## 3. Test Coverage <a name="3-coverage"></a>

### coverage.py Setup

```toml
# pyproject.toml
[tool.coverage.run]
source = ["app"]
branch = true
parallel = true
omit = [
    "app/migrations/*",
    "app/tests/*",
    "app/config.py",
]

[tool.coverage.report]
exclude_lines = [
    "pragma: no cover",
    "def __repr__",
    "if TYPE_CHECKING:",
    "if __name__ == .__main__.:",
    "raise NotImplementedError",
    "pass",
    "\\.\\.\\.",
]
fail_under = 80
show_missing = true
precision = 2
skip_covered = true

[tool.coverage.html]
directory = "htmlcov"

[tool.coverage.xml]
output = "coverage.xml"
```

### Running Coverage

```bash
# Basic coverage
pytest --cov=app

# With branch coverage
pytest --cov=app --cov-branch

# Generate reports
pytest --cov=app --cov-report=html --cov-report=xml --cov-report=term

# Minimum coverage threshold
pytest --cov=app --cov-fail-under=80

# Coverage for specific modules
pytest --cov=app.services --cov=app.routes

# Combine parallel coverage
coverage combine
coverage report
coverage html
```

### Coverage Configuration in CI

```yaml
# GitHub Actions with coverage
- name: Run tests with coverage
  run: |
    pytest \
      --cov=app \
      --cov-branch \
      --cov-report=xml:coverage.xml \
      --cov-report=html:htmlcov \
      --cov-report=term-missing \
      --cov-fail-under=80

- name: Upload coverage to Codecov
  uses: codecov/codecov-action@v4
  with:
    file: ./coverage.xml
    fail_ci_if_error: true
    flags: unittests
    name: codecov-umbrella
```

### Coverage Badges

```python
# Generate coverage badge
# pip install coverage-badge
# coverage-badge -o coverage.svg -f
```

```yaml
# Update badge in README
- name: Update coverage badge
  run: |
    coverage-badge -o assets/coverage-badge.svg -f
    git config --local user.email "action@github.com"
    git config --local user.name "GitHub Action"
    git add assets/coverage-badge.svg
    git diff --staged --quiet || git commit -m "Update coverage badge"
    git push
```

---

## 4. Test Reporting <a name="4-reporting"></a>

### JUnit XML Reports

```bash
# Generate JUnit XML report
pytest --junitxml=reports/junit.xml

# With test durations
pytest --junitxml=reports/junit.xml --durations=10

# In CI
pytest --junitxml=test-results.xml -v
```

### HTML Reports

```bash
pip install pytest-html

# Generate HTML report
pytest --html=reports/report.html --self-contained-html

# With custom CSS
pytest --html=reports/report.html --css=assets/style.css

# In CI - upload as artifact
- name: Upload test report
  uses: actions/upload-artifact@v4
  if: always()
  with:
    name: test-report
    path: reports/report.html
```

### Allure Reports

```bash
pip install allure-pytest

# Generate allure results
pytest --alluredir=allure-results

# Generate HTML report
allure serve allure-results

# In CI
- name: Generate Allure Report
  uses: simple-elf/allure-report-action@v1
  if: always()
  with:
    allure_results: allure-results
    allure_report: allure-report
    allure_history: allure-history

- name: Deploy report to Github Pages
  uses: peaceiris/actions-gh-pages@v3
  if: always()
  with:
    github_token: ${{ secrets.GITHUB_TOKEN }}
    publish_branch: gh-pages
    publish_dir: allure-report
```

### Custom Test Reporter

```python
# conftest.py
import json
import time
import pytest

class TestReport:
    def __init__(self):
        self.results = []
        self.start_time = time.time()

    @pytest.hookimpl(hookwrapper=True)
    def pytest_runtest_makereport(self, item, call):
        outcome = yield
        report = outcome.get_result()

        if report.when == "call":
            self.results.append({
                "name": item.nodeid,
                "outcome": report.outcome,
                "duration": report.duration,
                "failure_message": str(report.longrepr) if report.failed else None,
            })

    def pytest_sessionfinish(self, session, exitstatus):
        elapsed = time.time() - self.start_time

        summary = {
            "total": len(self.results),
            "passed": sum(1 for r in self.results if r["outcome"] == "passed"),
            "failed": sum(1 for r in self.results if r["outcome"] == "failed"),
            "skipped": sum(1 for r in self.results if r["outcome"] == "skipped"),
            "duration": elapsed,
            "results": self.results,
        }

        with open("test-report.json", "w") as f:
            json.dump(summary, f, indent=2)

reporter = TestReport()
```

---

## 5. Database Migrations in Tests <a name="5-migrations"></a>

### Alembic Migrations in Tests

```python
# conftest.py
import pytest
from alembic import command
from alembic.config import Config
from sqlalchemy import create_engine
from app.db import Base

@pytest.fixture(scope="session")
def db_engine():
    """Create test database and run migrations."""
    engine = create_engine("sqlite:///test.db")

    # Run migrations
    alembic_cfg = Config("alembic.ini")
    alembic_cfg.set_main_option("sqlalchemy.url", "sqlite:///test.db")
    command.upgrade(alembic_cfg, "head")

    yield engine

    # Cleanup
    command.downgrade(alembic_cfg, "base")
    import os
    os.remove("test.db")

@pytest.fixture(scope="session")
def db_session_factory(db_engine):
    return sessionmaker(bind=db_engine)

@pytest.fixture
def db_session(db_session_factory):
    session = db_session_factory()
    yield session
    session.rollback()
    session.close()
```

### Migration Testing

```python
# tests/test_migrations.py
import pytest
from alembic import command
from alembic.config import Config
from sqlalchemy import inspect

def test_migrations_apply_cleanly():
    """Verify migrations apply without errors."""
    engine = create_engine("sqlite:///migration_test.db")
    alembic_cfg = Config("alembic.ini")
    alembic_cfg.set_main_option("sqlalchemy.url", "sqlite:///migration_test.db")

    # Apply all migrations
    command.upgrade(alembic_cfg, "head")

    # Verify tables exist
    inspector = inspect(engine)
    tables = inspector.get_table_names()
    assert "users" in tables
    assert "items" in tables
    assert "orders" in tables

    # Cleanup
    command.downgrade(alembic_cfg, "base")
    import os
    os.remove("migration_test.db")

def test_migrations_rollback_cleanly():
    """Verify migrations can be fully rolled back."""
    alembic_cfg = Config("alembic.ini")
    alembic_cfg.set_main_option("sqlalchemy.url", "sqlite:///rollback_test.db")

    command.upgrade(alembic_cfg, "head")
    command.downgrade(alembic_cfg, "base")

    engine = create_engine("sqlite:///rollback_test.db")
    inspector = inspect(engine)
    tables = inspector.get_table_names()
    assert len(tables) == 0

    import os
    os.remove("rollback_test.db")

def test_migration_data_integrity():
    """Test that migration preserves data correctly."""
    alembic_cfg = Config("alembic.ini")
    alembic_cfg.set_main_option("sqlalchemy.url", "sqlite:///integrity_test.db")

    # Apply migrations and insert data
    command.upgrade(alembic_cfg, "head")
    engine = create_engine("sqlite:///integrity_test.db")

    with engine.connect() as conn:
        conn.execute(
            users_table.insert().values(name="Test User", email="test@test.com")
        )
        conn.commit()

    # Simulate migration to new version
    command.upgrade(alembic_cfg, "head")

    # Verify data is preserved
    with engine.connect() as conn:
        result = conn.execute(users_table.select()).fetchall()
        assert len(result) == 1
        assert result[0].name == "Test User"

    import os
    os.remove("integrity_test.db")
```

---

## 6. Docker-Based Testing <a name="6-docker"></a>

### Docker Compose for Testing

```yaml
# docker-compose.test.yml
version: "3.8"

services:
  api:
    build:
      context: .
      dockerfile: Dockerfile.test
    environment:
      - DATABASE_URL=postgresql+asyncpg://test:test@postgres:5432/test_db
      - REDIS_URL=redis://redis:6379
      - ENVIRONMENT=testing
    depends_on:
      postgres:
        condition: service_healthy
      redis:
        condition: service_healthy
    volumes:
      - ./tests:/app/tests
      - ./app:/app/app

  postgres:
    image: postgres:16
    environment:
      POSTGRES_USER: test
      POSTGRES_PASSWORD: test
      POSTGRES_DB: test_db
    ports:
      - "5432:5432"
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U test -d test_db"]
      interval: 5s
      timeout: 5s
      retries: 5

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 5s
      timeout: 5s
      retries: 5

  test-runner:
    build:
      context: .
      dockerfile: Dockerfile.test
    command: >
      pytest tests/ -v
      --tb=short
      --cov=app
      --cov-report=xml:/app/coverage.xml
      --junitxml=/app/test-results.xml
    environment:
      - DATABASE_URL=postgresql+asyncpg://test:test@postgres:5432/test_db
      - REDIS_URL=redis://redis:6379
    depends_on:
      postgres:
        condition: service_healthy
      redis:
        condition: service_healthy
    volumes:
      - ./test-results:/app/test-results
      - ./coverage.xml:/app/coverage.xml
```

### Dockerfile for Testing

```dockerfile
# Dockerfile.test
FROM python:3.12-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt requirements-test.txt ./
RUN pip install --no-cache-dir -r requirements.txt -r requirements-test.txt

# Copy application code
COPY . .

# Run tests
CMD ["pytest", "tests/", "-v", "--tb=short"]
```

### Running Tests in Docker

```bash
# Build and run tests
docker-compose -f docker-compose.test.yml up --build --abort-on-container-exit

# Run specific test type
docker-compose -f docker-compose.test.yml run test-runner pytest -m unit

# Run with coverage
docker-compose -f docker-compose.test.yml run test-runner \
  pytest --cov=app --cov-report=xml

# Cleanup
docker-compose -f docker-compose.test.yml down -v

# Parallel testing with Docker
docker-compose -f docker-compose.test.yml run test-runner \
  pytest -n auto --dist loadgroup
```

---

## 7. Test Environment Management <a name="7-environment"></a>

### Environment Configuration

```python
# config/test.py
import os

class TestConfig:
    DATABASE_URL = os.getenv(
        "TEST_DATABASE_URL",
        "sqlite:///./test.db"
    )
    REDIS_URL = os.getenv("TEST_REDIS_URL", "redis://localhost:6379/1")
    SECRET_KEY = "test-secret-key-not-for-production"
    TESTING = True
    DEBUG = True
    LOG_LEVEL = "DEBUG"

    # External services
    STRIPE_API_KEY = "sk_test_fake_key"
    SENDGRID_API_KEY = "SG.fake_key"
    AWS_ACCESS_KEY_ID = "fake_key"
    AWS_SECRET_ACCESS_KEY = "fake_secret"
```

### Environment Variables in CI

```yaml
# .github/workflows/ci.yml
env:
  DATABASE_URL: postgresql://test:test@localhost:5432/test_db
  REDIS_URL: redis://localhost:6379
  SECRET_KEY: test-secret-key-for-ci-only
  ENVIRONMENT: testing
  STRIPE_API_KEY: sk_test_fake
  SENDGRID_API_KEY: SG.fake

jobs:
  test:
    runs-on: ubuntu-latest
    env:
      DATABASE_URL: postgresql://test:test@localhost:5432/test_db
    steps:
      - name: Set test environment
        run: |
          echo "ENVIRONMENT=testing" >> $GITHUB_ENV
          echo "TESTING=true" >> $GITHUB_ENV
```

### Test Environment Fixtures

```python
# conftest.py
import os
import pytest

@pytest.fixture(autouse=True)
def test_environment():
    """Set up test environment variables."""
    os.environ["ENVIRONMENT"] = "testing"
    os.environ["TESTING"] = "true"
    os.environ["DEBUG"] = "true"

    yield

    # Cleanup
    os.environ.pop("ENVIRONMENT", None)
    os.environ.pop("TESTING", None)
    os.environ.pop("DEBUG", None)

@pytest.fixture(scope="session")
def setup_test_database():
    """Create test database schema."""
    from app.db import engine, Base

    Base.metadata.create_all(bind=engine)
    yield engine
    Base.metadata.drop_all(bind=engine)

@pytest.fixture(autouse=True)
def reset_database(setup_test_database):
    """Reset database state for each test."""
    from app.db import engine
    from sqlalchemy import text

    with engine.begin() as conn:
        # Truncate all tables
        for table in reversed(Base.metadata.sorted_tables):
            conn.execute(text(f"TRUNCATE TABLE {table.name} CASCADE"))

    yield
```

---

## 8. GitHub Actions Configuration <a name="8-github-actions"></a>

### Complete GitHub Actions CI

```yaml
# .github/workflows/ci.yml
name: CI

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

concurrency:
  group: ${{ github.workflow }}-${{ github.ref }}
  cancel-in-progress: true

jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.12"
          cache: pip
      - run: pip install ruff mypy
      - run: ruff check . --output-format=github
      - run: mypy app/ --strict

  test:
    runs-on: ubuntu-latest
    needs: lint
    strategy:
      matrix:
        python-version: ["3.11", "3.12"]
        test-type: [unit, integration]
    services:
      postgres:
        image: postgres:16
        env:
          POSTGRES_USER: test
          POSTGRES_PASSWORD: test
          POSTGRES_DB: test_db
        ports:
          - 5432:5432
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: ${{ matrix.python-version }}
          cache: pip
      - run: pip install -e ".[test]"
      - name: Run unit tests
        if: matrix.test-type == 'unit'
        run: pytest tests/unit/ -v --cov=app --cov-report=xml
      - name: Run integration tests
        if: matrix.test-type == 'integration'
        run: pytest tests/integration/ -v --cov=app --cov-report=xml
        env:
          DATABASE_URL: postgresql://test:test@localhost:5432/test_db
      - uses: codecov/codecov-action@v4
        if: matrix.python-version == '3.12'
        with:
          file: ./coverage.xml

  security:
    runs-on: ubuntu-latest
    needs: lint
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.12"
      - run: pip install safety bandit
      - run: safety check -r requirements.txt
      - run: bandit -r app/ -f json -o bandit-report.json || true

  deploy-staging:
    runs-on: ubuntu-latest
    needs: [test, security]
    if: github.ref == 'refs/heads/main'
    environment: staging
    steps:
      - uses: actions/checkout@v4
      - name: Deploy to staging
        run: echo "Deploying to staging..."
```

---

## 9. GitLab CI Configuration <a name="9-gitlab-ci"></a>

```yaml
# .gitlab-ci.yml
stages:
  - lint
  - test
  - security
  - deploy

variables:
  PIP_CACHE_DIR: "$CI_PROJECT_DIR/.pip-cache"
  POSTGRES_DB: test_db
  POSTGRES_USER: test
  POSTGRES_PASSWORD: test

cache:
  key: ${CI_COMMIT_REF_SLUG}
  paths:
    - .pip-cache/

lint:
  stage: lint
  image: python:3.12
  before_script:
    - pip install ruff mypy
  script:
    - ruff check .
    - mypy app/

test:unit:
  stage: test
  image: python:3.12
  before_script:
    - pip install -e ".[test]"
  script:
    - pytest tests/unit/ -v --cov=app --cov-report=xml
  coverage: '/TOTAL.*\s+(\d+)%/'
  artifacts:
    reports:
      coverage_report:
        coverage_format: cobertura
        path: coverage.xml
      junit: test-results.xml

test:integration:
  stage: test
  image: python:3.12
  services:
    - postgres:16
  before_script:
    - pip install -e ".[test]"
  script:
    - alembic upgrade head
    - pytest tests/integration/ -v --junitxml=test-results.xml
  variables:
    DATABASE_URL: postgresql://test:test@postgres:5432/test_db
  artifacts:
    reports:
      junit: test-results.xml

security:
  stage: security
  image: python:3.12
  before_script:
    - pip install safety bandit
  script:
    - safety check -r requirements.txt
    - bandit -r app/

deploy:staging:
  stage: deploy
  only:
    - main
  script:
    - echo "Deploying to staging..."
  environment:
    name: staging
```

---

## 10. Test Performance Optimization <a name="10-optimization"></a>

### Fast Test Strategies

```python
# 1. Use in-memory database
@pytest.fixture(scope="session")
def fast_engine():
    return create_engine("sqlite://", poolclass=StaticPool)

# 2. Share expensive setup across tests
@pytest.fixture(scope="module")
def populated_db(fast_engine):
    """Populate database once per module."""
    Base.metadata.create_all(bind=fast_engine)
    with fast_engine.begin() as conn:
        conn.execute(users_table.insert(), [
            {"name": f"User {i}", "email": f"user{i}@test.com"}
            for i in range(100)
        ])
    yield fast_engine
    Base.metadata.drop_all(bind=fast_engine)

# 3. Mock expensive operations
@pytest.fixture
def mock_slow_api(mocker):
    return mocker.patch(
        "app.services.slow_external_api",
        return_value={"data": "mocked"}
    )

# 4. Use factory-boy for test data
from factories import UserFactory, ItemFactory

def test_create_order(client):
    user = UserFactory.build()
    item = ItemFactory.build()
    # ... test code
```

### Profiling Tests

```bash
# Find slow tests
pytest --durations=10

# Profile with cProfile
python -m cProfile -o test_profile.prof -m pytest tests/

# Analyze profile
python -c "
import pstats
stats = pstats.Stats('test_profile.prof')
stats.sort_stats('cumulative')
stats.print_stats(20)
"

# Use pytest-profiling
pip install pytest-profiling
pytest --profile --profile-svg
```

### Test Caching

```python
# Use pytest-cache for test results
# pip install pytest-cache

# Cache expensive fixtures
@pytest.fixture(scope="session")
def expensive_computation():
    """Result is cached across the test session."""
    return perform_expensive_calculation()

# Cache database state
@pytest.fixture(scope="session")
def database_snapshot():
    """Take a database snapshot for fast restoration."""
    snapshot = take_snapshot()
    yield snapshot
    restore_snapshot(snapshot)
```

---

## 11. Flaky Test Management <a name="11-flaky"></a>

### Identifying Flaky Tests

```python
# Mark flaky tests
import pytest

@pytest.mark.flaky(reruns=3, reruns_delay=2)
def test_sometimes_fails():
    """This test might fail due to timing issues."""
    import random
    assert random.random() > 0.1  # 90% pass rate

# Or use pytest-rerunfailures
# pip install pytest-rerunfailures

@pytest.mark.flaky(reruns=3, reruns_delay=2)
async def test_async_operation(client):
    """Retry flaky async tests."""
    response = await client.get("/slow-endpoint")
    assert response.status_code == 200
```

### CI Configuration for Flaky Tests

```yaml
# Track flaky tests in CI
- name: Run tests with retry
  run: |
    pytest tests/ \
      --reruns 3 \
      --reruns-delay 2 \
      --junitxml=test-results.xml

- name: Publish test results
  uses: dorny/test-reporter@v1
  if: always()
  with:
    name: Test Results
    path: test-results.xml
    reporter: java-junit
```

### Root Causes and Fixes

```python
# Problem: Race condition
# Fix: Add proper waits and synchronization
async def test_order_processing(client):
    response = await client.post("/orders/", json={...})
    assert response.status_code == 201

    # Instead of sleep(1), use polling
    for _ in range(10):
        status_response = await client.get(f"/orders/{order_id}")
        if status_response.json()["status"] == "completed":
            break
        await asyncio.sleep(0.1)

# Problem: Shared state
# Fix: Use isolated test data
def test_with_unique_data(client):
    import uuid
    unique_name = f"Test {uuid.uuid4()}"
    response = client.post("/items/", json={"name": unique_name})
    assert response.status_code == 201

# Problem: Time-dependent
# Fix: Mock time
def test_token_expiry(mocker):
    from datetime import datetime
    mock_time = mocker.patch("app.auth.datetime")
    mock_time.now.return_value = datetime(2024, 1, 1, 12, 0, 0)
    # Test token at specific time
```

---

## 12. Security Testing in CI <a name="12-security"></a>

### Security Scan Tools

```yaml
# .github/workflows/security.yml
name: Security

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  dependency-scan:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.12"
      - run: pip install safety pip-audit
      - run: safety check -r requirements.txt
      - run: pip-audit -r requirements.txt

  sast:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.12"
      - run: pip install bandit semgrep
      - run: bandit -r app/ -f json -o bandit-report.json
      - run: semgrep --config=auto --json --output=semgrep-report.json app/

  secret-scan:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0
      - uses: trufflesecurity/trufflehog@main
        with:
          extra_args: --only-verified

  container-scan:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Build Docker image
        run: docker build -t myapp:test .
      - name: Scan with Trivy
        uses: aquasecurity/trivy-action@master
        with:
          image-ref: myapp:test
          format: json
          output: trivy-report.json
```

### Bandit Security Linter

```bash
# Install and run
pip install bandit

# Run on app directory
bandit -r app/

# With specific severity
bandit -r app/ -ll  # Medium and above

# Generate JSON report
bandit -r app/ -f json -o bandit-report.json

# Exclude test files
bandit -r app/ --exclude app/tests/
```

### OWASP ZAP Integration

```yaml
# Docker-based ZAP scan
- name: OWASP ZAP Scan
  uses: zaproxy/action-full-scan@v0.10.0
  with:
    target: http://localhost:8000
    rules_file_name: '.zap/rules.tsv'
    cmd_options: '-a'
```

---

## 13. Best Practices <a name="13-best-practices"></a>

### 1. Test on Every PR

```yaml
on:
  pull_request:
    branches: [main]
# Every PR must pass tests before merge
```

### 2. Cache Dependencies

```yaml
- uses: actions/setup-python@v5
  with:
    python-version: "3.12"
    cache: pip
```

### 3. Run Tests in Parallel

```bash
# Use pytest-xdist for parallel execution
pytest -n auto
```

### 4. Separate Test Types

```bash
# Unit tests: Fast, no dependencies
pytest tests/unit/ -v

# Integration tests: Need DB, external services
pytest tests/integration/ -v

# E2E tests: Full stack
pytest tests/e2e/ -v
```

### 5. Fail Fast in CI

```yaml
steps:
  - run: pytest -x  # Stop on first failure
```

### 6. Generate Reports

```yaml
- run: pytest --junitxml=results.xml --cov=app --cov-report=xml
- uses: actions/upload-artifact@v4
  with:
    name: test-results
    path: results.xml
```

### 7. Monitor Test Health

```bash
# Track test duration
pytest --durations=10

# Track flaky tests
pytest --reruns 3 --reruns-delay 2

# Monitor coverage trends
pytest --cov=app --cov-report=html
```

---

## Summary

| Concept | Key Point |
|---------|-----------|
| CI/CD | Automated testing on every PR |
| Parallel | pytest-xdist for speed |
| Coverage | Track and enforce minimum thresholds |
| Reporting | JUnit XML, HTML, Allure |
| Migrations | Alembic in test setup |
| Docker | Consistent test environments |
| Environment | Separate test config from production |
| Flaky Tests | Identify, retry, and fix root causes |
| Security | Bandit, safety, semgrep in CI |

### CI Checklist

- [ ] Linting (ruff, mypy)
- [ ] Unit tests (fast, no dependencies)
- [ ] Integration tests (DB, Redis)
- [ ] Coverage report (>80%)
- [ ] Security scan (bandit, safety)
- [ ] Docker build test
- [ ] Test report artifacts
- [ ] Deployment readiness
