# Document AI

A pipeline for downloading academic papers from arXiv and extracting structured content using vision-language models. Built with [DeepSeek-OCR-2](https://huggingface.co/deepseek-ai/DeepSeek-OCR-2) as the default OCR engine, but designed with a ports & adapters architecture to support any document AI model.

<img width="800" height="478" alt="image" src="https://github.com/user-attachments/assets/76046000-0a59-4400-a086-e5d16bb2f060" />


## What it does

1. **Search & Download** - Queries the arXiv API and downloads papers as PDFs
2. **PDF to Images** - Converts each PDF page into high-resolution images
3. **OCR & Extraction** - Runs a vision-language model on each page to extract:
   - Markdown text
   - Bounding-box annotated page images
   - Cropped figures
4. **Store** - Saves metadata to DuckDB and artifacts to the local filesystem

## Architecture

The project follows a hexagonal (ports & adapters) architecture, making it easy to swap out components:

```
interface/          Entrypoints & dependency wiring
application/        Business logic & port definitions (ABCs)
infrastructure/     Concrete implementations
domain/             Core data models
```

| Port | Default Implementation | Description |
|---|---|---|
| `IParserService` | `DeepseekOCRParser` | OCR model for page parsing |
| `IDocumentSourceService` | `ArxivDocumentSourceService` | Paper discovery & metadata |
| `IStorageService` | `LocalStorageService` | File storage for PDFs & images |
| `IDBService` | `DuckDBService` | Metadata persistence |

To add a new OCR model, implement the `IParserService` interface and wire it in `interface/dependencies.py`.

## Prerequisites

- Python >= 3.12
- [uv](https://docs.astral.sh/uv/) - Python package manager
- [just](https://github.com/casey/just) - Command runner
- NVIDIA GPU with CUDA (required for model inference)

## Quickstart

```bash
# Clone the repository
git clone https://github.com/jeremyarancio/document-ai.git
cd document-ai

# Install system dependencies (just, duckdb CLI) and set up the project
just init

# (Optional) Install GPU dependencies for model inference
uv sync --extra gpu
```

## Usage

The pipeline exposes two main entrypoints in `src/document_ai/interface/entrypoints.py`:

```python
from document_ai.interface.entrypoints import download_arxiv_papers, parse_documents

# Step 1: Download papers from arXiv
download_arxiv_papers()

# Step 2: Parse downloaded papers with OCR
parse_documents()
```

## Development

```bash
# Format & lint
just format

# Type check
just type-check

# Run both before committing
just pre-commit

# Run tests
uv run pytest

# List all available recipes
just
```
