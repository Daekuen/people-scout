from __future__ import annotations

import asyncio
import sys
from pathlib import Path

import click
from rich.console import Console

from people_scout.analysis.models import PersonReport
from people_scout.output.console import ConsoleRenderer
from people_scout.output.json_writer import write_json
from people_scout.output.markdown import write_markdown

console = Console()


@click.command()
@click.argument("handle")
@click.option("--lang", "-l", type=click.Choice(["ko", "en"]), default="ko", help="리포트 언어")
@click.option(
    "--output", "-o", "output_formats", default="console",
    help="출력 형식 (쉼표 구분: console, json, markdown)",
)
@click.option("--post-count", "-p", type=int, default=100, help="수집할 포스트 수")
@click.option("--output-dir", type=click.Path(), default=".", help="파일 출력 디렉토리")
def main(
    handle: str,
    lang: str,
    output_formats: str,
    post_count: int,
    output_dir: str,
) -> None:
    """People Scout - 트위터 인물 인텔리전스 리포트 생성기.

    HANDLE: 분석 대상 트위터 핸들 (예: @kimceo)
    """
    console.print("\n[bold cyan] People Scout v0.1.0[/]\n")

    formats = [f.strip() for f in output_formats.split(",")]

    try:
        report = asyncio.run(_run_analysis(handle, lang, post_count))
    except KeyboardInterrupt:
        console.print("\n[yellow]분석이 취소되었습니다.[/]")
        sys.exit(1)
    except Exception as e:
        console.print(f"\n[bold red]Error:[/] {e}")
        sys.exit(1)

    _output_report(report, formats, output_dir)


async def _run_analysis(
    handle: str,
    lang: str,
    post_count: int,
) -> PersonReport:
    from people_scout.scout import PeopleScout

    scout = PeopleScout()

    steps = ["profile", "posts", "analysis"]
    step_labels = {
        "profile": "프로필 수집 중",
        "posts": "포스트 수집 중",
        "analysis": "Gemini 분석 중",
    }

    def on_progress(step: str, status: str) -> None:
        if status == "start":
            idx = steps.index(step) + 1 if step in steps else 0
            label = step_labels.get(step, step)
            console.print(f"  [dim][{idx}/{len(steps)}][/] {label}...", end="")
        elif status == "done":
            console.print(" [green]done[/]")

    report = await scout.analyze_async(
        handle,
        lang=lang,
        post_count=post_count,
        on_progress=on_progress,
    )
    console.print()
    return report


def _output_report(report: PersonReport, formats: list[str], output_dir: str) -> None:
    handle_clean = report.handle.lstrip("@")
    out_path = Path(output_dir)
    out_path.mkdir(parents=True, exist_ok=True)

    if "console" in formats:
        renderer = ConsoleRenderer(console)
        renderer.render(report)

    if "json" in formats:
        json_path = out_path / f"{handle_clean}_report.json"
        write_json(report, json_path)
        console.print(f"  [dim]JSON 저장: {json_path}[/]")

    if "markdown" in formats:
        md_path = out_path / f"{handle_clean}_report.md"
        write_markdown(report, md_path)
        console.print(f"  [dim]마크다운 저장: {md_path}[/]")
