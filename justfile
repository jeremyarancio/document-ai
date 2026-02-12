default:
    @just --list

type-check:
    uvx ty check .

format:
    uvx ruff check --fix .
    uvx ruff format .

pre-commit: type-check format