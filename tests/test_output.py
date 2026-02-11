from __future__ import annotations

from datetime import datetime, timezone

from rich.console import Console

from people_scout.analysis.models import (
    CommunicationStyle,
    ContentTypeRatio,
    ConversationEntry,
    InterestItem,
    PersonReport,
)
from people_scout.output.console import ConsoleRenderer
from people_scout.output.json_writer import write_json
from people_scout.output.markdown import render_markdown, write_markdown


def _make_report() -> PersonReport:
    return PersonReport(
        handle="@testuser",
        display_name="Test User",
        bio="AI researcher",
        summary="An AI researcher building the future.",
        recent_interests=[
            InterestItem(topic="AI", frequency="high", sentiment="positive", evidence="Talks about AI"),
        ],
        communication_style=CommunicationStyle(
            tone="professional",
            tone_description="Professional and insightful",
            post_frequency="active",
            active_hours="9-11am, 8-10pm",
            content_type_ratio=ContentTypeRatio(original=60, retweet=20, reply=15, quote=5),
            engagement_style="Actively replies to relevant threads",
            language_mix=["Korean", "English"],
        ),
        conversation_entry_points=[
            ConversationEntry(
                topic="AI Research",
                reason="Core interest",
                suggested_approach="Ask about latest research",
                confidence="high",
            ),
        ],
        collected_at=datetime.now(timezone.utc),
        post_count=100,
        api_calls=2,
        duration_seconds=12.5,
    )


def test_console_render_no_crash():
    report = _make_report()
    console = Console(file=None, force_terminal=True)
    renderer = ConsoleRenderer(console)
    renderer.render(report)


def test_render_markdown():
    report = _make_report()
    md = render_markdown(report)
    assert "# 인물 리포트: Test User (@testuser)" in md
    assert "## 요약" in md
    assert "## 최근 관심사" in md
    assert "## 소통 스타일" in md
    assert "## 대화 진입점" in md


def test_write_json(tmp_path):
    report = _make_report()
    path = write_json(report, tmp_path / "output.json")
    assert path.exists()
    restored = PersonReport.model_validate_json(path.read_text())
    assert restored.handle == "@testuser"


def test_write_markdown(tmp_path):
    report = _make_report()
    path = write_markdown(report, tmp_path / "output.md")
    assert path.exists()
    assert "Test User" in path.read_text()
