from __future__ import annotations

from pathlib import Path

from people_scout.analysis.models import PersonReport


def render_markdown(report: PersonReport) -> str:
    """PersonReport를 마크다운 문자열로 렌더링한다."""
    lines: list[str] = []

    # 헤더
    lines.append(f"# 인물 리포트: {report.display_name} ({report.handle})")
    lines.append("")
    if report.bio:
        lines.append(f"> {report.bio}")
        lines.append("")
    lines.append(f"*분석 시각: {report.collected_at.strftime('%Y-%m-%d %H:%M UTC')}*")
    lines.append("")

    # 요약
    lines.append("## 요약")
    lines.append("")
    lines.append(report.summary)
    lines.append("")

    # 최근 관심사
    lines.append("## 최근 관심사")
    lines.append("")
    lines.append("| 주제 | 빈도 | 감성 | 근거 |")
    lines.append("|------|------|------|------|")
    for item in report.recent_interests:
        lines.append(f"| {item.topic} | {item.frequency} | {item.sentiment} | {item.evidence} |")
    lines.append("")

    # 소통 스타일
    style = report.communication_style
    ratio = style.content_type_ratio
    lines.append("## 소통 스타일")
    lines.append("")
    lines.append(f"- **톤**: {style.tone} — {style.tone_description}")
    lines.append(f"- **빈도**: {style.post_frequency}")
    lines.append(f"- **활동 시간**: {style.active_hours}")
    lines.append(
        f"- **콘텐츠 비율**: 오리지널 {ratio.original}% / RT {ratio.retweet}% / "
        f"답글 {ratio.reply}% / 인용 {ratio.quote}%"
    )
    lines.append(f"- **상호작용**: {style.engagement_style}")
    lines.append(f"- **언어**: {', '.join(style.language_mix)}")
    lines.append("")

    # 대화 진입점
    lines.append("## 대화 진입점")
    lines.append("")
    for i, entry in enumerate(report.conversation_entry_points, 1):
        lines.append(f"### {i}. {entry.topic} `{entry.confidence}`")
        lines.append("")
        lines.append(f"**이유**: {entry.reason}")
        lines.append("")
        lines.append(f"**접근법**: *\"{entry.suggested_approach}\"*")
        lines.append("")

    # 메타데이터
    lines.append("---")
    lines.append("")
    lines.append(
        f"*{report.duration_seconds}초 소요 | API {report.api_calls}회 | "
        f"포스트 {report.post_count}개 분석*"
    )

    return "\n".join(lines)


def write_markdown(report: PersonReport, path: str | Path) -> Path:
    """PersonReport를 마크다운 파일로 저장한다."""
    path = Path(path)
    path.write_text(render_markdown(report), encoding="utf-8")
    return path
