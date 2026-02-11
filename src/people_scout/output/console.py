from __future__ import annotations

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

from people_scout.analysis.models import PersonReport


class ConsoleRenderer:
    """Rich 기반 터미널 리포트 렌더러."""

    def __init__(self, console: Console | None = None):
        self.console = console or Console()

    def render(self, report: PersonReport) -> None:
        self.console.print()
        self._render_header(report)
        self._render_summary(report)
        self._render_interests(report)
        self._render_communication_style(report)
        self._render_conversation_entries(report)
        self._render_footer(report)

    def _render_header(self, report: PersonReport) -> None:
        title = f"인물 리포트: {report.display_name} ({report.handle})"
        self.console.rule(f"[bold cyan]{title}[/]")
        if report.bio:
            self.console.print(f"  [dim]{report.bio}[/]")
        self.console.print()

    def _render_summary(self, report: PersonReport) -> None:
        self.console.print(
            Panel(report.summary, title="[bold]요약[/]", border_style="green")
        )

    def _render_interests(self, report: PersonReport) -> None:
        table = Table(title="최근 관심사", show_header=True)
        table.add_column("주제", style="bold")
        table.add_column("빈도", justify="center")
        table.add_column("감성", justify="center")
        table.add_column("근거")

        freq_style = {"high": "red", "medium": "yellow", "low": "dim"}
        sent_style = {"positive": "green", "negative": "red", "neutral": "dim", "mixed": "yellow"}

        for item in report.recent_interests:
            table.add_row(
                item.topic,
                Text(item.frequency, style=freq_style.get(item.frequency, "")),
                Text(item.sentiment, style=sent_style.get(item.sentiment, "")),
                item.evidence[:60] + ("..." if len(item.evidence) > 60 else ""),
            )
        self.console.print(table)
        self.console.print()

    def _render_communication_style(self, report: PersonReport) -> None:
        style = report.communication_style
        ratio = style.content_type_ratio

        lines = [
            f"[bold]톤:[/] {style.tone} — {style.tone_description}",
            f"[bold]빈도:[/] {style.post_frequency} | [bold]활동 시간:[/] {style.active_hours}",
            f"[bold]콘텐츠:[/] 오리지널 {ratio.original}% | RT {ratio.retweet}% | 답글 {ratio.reply}% | 인용 {ratio.quote}%",
            f"[bold]상호작용:[/] {style.engagement_style}",
            f"[bold]언어:[/] {', '.join(style.language_mix)}",
        ]
        self.console.print(Panel("\n".join(lines), title="[bold]소통 스타일[/]", border_style="blue"))

    def _render_conversation_entries(self, report: PersonReport) -> None:
        self.console.print("[bold]대화 진입점[/]")
        for i, entry in enumerate(report.conversation_entry_points, 1):
            conf_style = {"high": "green", "medium": "yellow", "low": "dim"}
            conf_text = Text(f"[{entry.confidence}]", style=conf_style.get(entry.confidence, ""))
            self.console.print(f"  {i}. [bold]{entry.topic}[/] ", end="")
            self.console.print(conf_text)
            self.console.print(f"     {entry.reason}")
            self.console.print(f"     [italic]\"{entry.suggested_approach}\"[/]")
        self.console.print()

    def _render_footer(self, report: PersonReport) -> None:
        self.console.print(
            f"[dim]완료 ({report.duration_seconds}초, API {report.api_calls}회, "
            f"포스트 {report.post_count}개 분석)[/]"
        )
        self.console.print()
