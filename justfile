db_path := "data/duck.db"

# List and run recipes interactively
default:
    @just --choose

# Install system dependencies and set up the project
init:
    @echo "Installing duckdb CLI..."
    @which duckdb > /dev/null 2>&1 || (curl -fsSL https://install.duckdb.org | sh)
    @echo "Setting up Python environment with uv..."
    uv sync
    @mkdir -p data/storage
    @echo "Running migrations..."
    @just migrate
    @echo "Setup complete! Run 'just' to see available recipes."

# Run type checking with ty
type-check:
    @echo "🔍 Running type checks..."
    uvx ty check .
    @echo "✅ Type checks passed!"

# Lint (with auto-fix) and format code with ruff
format:
    @echo "🧹 Linting and fixing..."
    uvx ruff check --fix .
    @echo "🎨 Formatting..."
    uvx ruff format .
    @echo "✅ Format complete!"

# Run type-check and format before committing
pre-commit: format type-check
    @echo "🚀 Pre-commit checks passed!"

# Run all SQL migrations against the DuckDB database
migrate:
    @echo "📦 Running migrations against {{db_path}}..."
    for f in migrations/*.sql; do echo "  Running $f..."; duckdb {{db_path}} < "$f"; done
    @echo "✅ Migrations complete!"