from __future__ import annotations

import json
from pathlib import Path

import pytest

FIXTURES_DIR = Path(__file__).parent / "fixtures"


@pytest.fixture
def profile_response() -> dict:
    return json.loads((FIXTURES_DIR / "twitter_profile.json").read_text())


@pytest.fixture
def posts_response() -> dict:
    return json.loads((FIXTURES_DIR / "twitter_posts.json").read_text())


@pytest.fixture
def profile_data(profile_response: dict) -> dict:
    """프로필 데이터 (실제 API는 트윗 리스트를 반환하므로, 프롬프트용 dict로 변환)."""
    tweets = profile_response["data"]["result"]
    # scout.py에서 analyzer에 전달하는 형식과 동일
    username = tweets[0]["username"] if tweets else "testuser"
    return {"handle": username}


@pytest.fixture
def posts_data(posts_response: dict) -> dict:
    """포스트 데이터 (프롬프트 빌더용 dict)."""
    result = posts_response["data"]["result"]
    # TWITTER_POST: {post: {}, reply: [tweets]}
    tweets = result.get("reply", [])
    return {"posts": tweets}
