import re
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parents[1]
_SOURCE_ID_PATTERN = re.compile(r"\[((?:BR|SC|WI|DI|SA|CP|BF|AT|SH)-[A-Z0-9-]+)\]")
_SOURCE_RECORD_PATTERN = re.compile(
    r"^### \[((?:BR|SC|WI|DI|SA|CP|BF|AT|SH)-[A-Z0-9-]+)\]",
    re.MULTILINE,
)


def _maintained_source_consumers() -> list[Path]:
    reference_dir = _REPO_ROOT / "docs" / "reference"
    return [
        _REPO_ROOT / "README.md",
        _REPO_ROOT / "ROADMAP.md",
        _REPO_ROOT / "DESIGN.md",
        _REPO_ROOT / "docs" / "asbc-verification.md",
        *sorted(reference_dir.glob("*.md")),
    ]


def test_maintained_source_ids_exist_in_master_ledger() -> None:
    ledger_text = (_REPO_ROOT / "docs" / "sources.md").read_text()
    ledger_ids = set(_SOURCE_RECORD_PATTERN.findall(ledger_text))

    missing_by_file: dict[str, list[str]] = {}
    for path in _maintained_source_consumers():
        cited_ids = set(_SOURCE_ID_PATTERN.findall(path.read_text()))
        missing = sorted(cited_ids - ledger_ids)
        if missing:
            missing_by_file[str(path.relative_to(_REPO_ROOT))] = missing

    assert not missing_by_file, missing_by_file


def test_master_source_ledger_has_unique_ids() -> None:
    ledger_text = (_REPO_ROOT / "docs" / "sources.md").read_text()
    ledger_ids = _SOURCE_RECORD_PATTERN.findall(ledger_text)

    assert len(ledger_ids) == len(set(ledger_ids))
