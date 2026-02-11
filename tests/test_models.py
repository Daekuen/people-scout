from __future__ import annotations

from datetime import datetime, timezone

from people_scout.analysis.models import (
    CommunicationStyle,
    ContentTypeRatio,
    ConversationEntry,
    InterestItem,
    PersonReport,
)


def _make_report(**overrides) -> PersonReport:
    defaults = dict(
        handle="@testuser",
        display_name="Test User",
        bio="AI researcher",
        summary="Test summary",
        recent_interests=[
            InterestItem(topic="AI", frequency="high", sentiment="positive", evidence="Posts about AI"),
        ],
        communication_style=CommunicationStyle(
            tone="professional",
            tone_description="Professional tone",
            post_frequency="active",
            active_hours="9-11am",
            content_type_ratio=ContentTypeRatio(original=60, retweet=20, reply=15, quote=5),
            engagement_style="Active engagement",
            language_mix=["Korean", "English"],
        ),
        conversation_entry_points=[
            ConversationEntry(
                topic="AI Research",
                reason="Frequently discusses AI",
                suggested_approach="Ask about latest AI trends",
                confidence="high",
            ),
        ],
        collected_at=datetime.now(timezone.utc),
        post_count=100,
        api_calls=2,
        duration_seconds=12.5,
    )
    defaults.update(overrides)
    return PersonReport(**defaults)


def test_person_report_creation():
    report = _make_report()
    assert report.handle == "@testuser"
    assert report.display_name == "Test User"
    assert len(report.recent_interests) == 1


def test_person_report_json_serialization():
    report = _make_report()
    json_str = report.model_dump_json()
    assert "@testuser" in json_str

    restored = PersonReport.model_validate_json(json_str)
    assert restored.handle == report.handle
    assert restored.summary == report.summary


def test_person_report_to_json(tmp_path):
    report = _make_report()
    path = tmp_path / "test_report.json"
    report.to_json(path)
    assert path.exists()

    restored = PersonReport.model_validate_json(path.read_text())
    assert restored.handle == "@testuser"


def test_person_report_to_markdown(tmp_path):
    report = _make_report()
    path = tmp_path / "test_report.md"
    report.to_markdown(path)
    assert path.exists()
    content = path.read_text()
    assert "Test User" in content
    assert "@testuser" in content
