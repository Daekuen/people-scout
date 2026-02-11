from __future__ import annotations

from pathlib import Path

from people_scout.analysis.models import PersonReport


def write_json(report: PersonReport, path: str | Path) -> Path:
    """PersonReport를 JSON 파일로 저장한다."""
    path = Path(path)
    path.write_text(report.model_dump_json(indent=2), encoding="utf-8")
    return path
