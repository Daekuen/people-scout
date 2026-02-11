from __future__ import annotations

from typing import Any


SYSTEM_INSTRUCTION_TEMPLATE = """\
You are an expert person intelligence analyst. Your job is to analyze \
Twitter/X data about a person and produce a structured intelligence report.

Rules:
1. Base all analysis strictly on the provided data. Do not hallucinate.
2. When evidence is insufficient, say so explicitly rather than guessing.
3. For sentiment analysis, consider context and nuance.
4. Provide actionable conversation entry points based on concrete evidence.
5. NEVER reference internal post numbers like [1], [2], [3] in your output. \
The reader has no access to the raw data. Instead, describe the evidence \
by summarizing actual post content (e.g., "tweeted about launching a free education platform").
6. Output language: {lang_full}"""

LANG_MAP = {
    "ko": "Korean",
    "en": "English",
}


def build_system_instruction(lang: str = "ko") -> str:
    lang_full = LANG_MAP.get(lang, "Korean")
    return SYSTEM_INSTRUCTION_TEMPLATE.format(lang_full=lang_full)


def build_user_prompt(
    profile: dict[str, Any],
    posts: dict[str, Any] | None = None,
) -> str:
    sections: list[str] = []

    # 프로필 섹션
    sections.append(_format_profile(profile))

    # 포스트 섹션
    if posts:
        sections.append(_format_posts(posts))

    # 분석 요청
    sections.append(_analysis_instruction())

    return "\n\n".join(sections)


def _format_profile(profile: dict[str, Any]) -> str:
    lines = ["## Target Person"]
    field_map = [
        ("Handle", "handle", lambda v: f"@{v}" if not str(v).startswith("@") else v),
        ("Display Name", "displayName", None),
        ("Bio", "bio", None),
        ("Followers", "followersCount", lambda v: f"{v:,}" if isinstance(v, int) else v),
        ("Following", "followingCount", lambda v: f"{v:,}" if isinstance(v, int) else v),
        ("Posts", "postsCount", lambda v: f"{v:,}" if isinstance(v, int) else v),
        ("Join Date", "joinDate", None),
        ("Location", "location", None),
        ("Website", "website", None),
        ("Verified", "verified", None),
    ]
    for label, key, fmt in field_map:
        val = profile.get(key)
        if val is not None:
            lines.append(f"{label}: {fmt(val) if fmt else val}")
    return "\n".join(lines)


def _format_posts(posts: dict[str, Any]) -> str:
    items = posts.get("posts", posts.get("tweets", []))
    if not items:
        return "## Recent Posts\nNo posts available."

    lines = [f"## Recent Posts ({len(items)} posts)"]
    for i, post in enumerate(items, 1):
        # 실제 Selanet API 필드: content, postedAt, likesCount, retweetsCount, repliesCount
        text = post.get("content", post.get("text", ""))
        date = post.get("postedAt", post.get("date", post.get("createdAt", "")))
        likes = post.get("likesCount", post.get("likes", post.get("likeCount", 0)))
        rts = post.get("retweetsCount", post.get("retweets", post.get("retweetCount", 0)))
        replies = post.get("repliesCount", post.get("replies", post.get("replyCount", 0)))

        lines.append(f"[{i}] {date} | Likes: {likes} | RTs: {rts} | Replies: {replies}")
        lines.append(text)
        lines.append("---")
    return "\n".join(lines)


def _analysis_instruction() -> str:
    focus = [
        "1. A concise 2-3 sentence summary of who this person is",
        "2. Their recent interests with frequency and sentiment",
        "3. Their communication style and patterns",
        "4. Actionable conversation entry points",
    ]
    return (
        "---\n\nAnalyze this person and generate a comprehensive intelligence report.\n"
        "Focus on:\n" + "\n".join(focus)
    )
