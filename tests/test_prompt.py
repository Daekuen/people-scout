from __future__ import annotations

from people_scout.analysis.prompt import (
    build_system_instruction,
    build_user_prompt,
)


def test_system_instruction_korean():
    result = build_system_instruction("ko")
    assert "Korean" in result
    assert "expert person intelligence analyst" in result


def test_system_instruction_english():
    result = build_system_instruction("en")
    assert "English" in result


def test_build_user_prompt_profile_only(profile_data: dict):
    result = build_user_prompt(profile_data)
    assert "## Target Person" in result
    assert "testuser" in result


def test_build_user_prompt_with_posts(profile_data: dict, posts_data: dict):
    result = build_user_prompt(profile_data, posts=posts_data)
    assert "## Recent Posts" in result
    assert "LLM agents" in result
