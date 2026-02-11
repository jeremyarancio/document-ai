import json
from pathlib import Path

import pytest

from document_ai.infrastructure.schemas.docsource import ArxivDocuments


DATAPATH = Path("tests/unittests/data/arxiv.json")
DATAPATH_WITH_VALIDATION_ERROR = Path("tests/unittests/data/arxiv_without_pdf.json")


def test_validate_arxiv():
    with DATAPATH.open("r") as f:
        data = json.load(f)
        ArxivDocuments.model_validate(data)


def test_validate_arxiv_missing_pdf():
    with DATAPATH_WITH_VALIDATION_ERROR.open("r") as f:
        data = json.load(f)
        with pytest.raises(ValueError):
            ArxivDocuments.model_validate(data)
