from __future__ import annotations

import json
from pathlib import Path

import httpx
import pytest
import respx

from people_scout.selanet.client import SelanetClient
from people_scout.selanet.errors import (
    ProfileNotFoundError,
    SelanetAuthError,
    SelanetScrapeError,
)
from people_scout.selanet.rate_limiter import AsyncRateLimiter

FIXTURES_DIR = Path(__file__).parent / "fixtures"
BASE_URL = "https://test-selanet.com"


@pytest.fixture
def client() -> SelanetClient:
    return SelanetClient(
        api_key="test-key",
        base_url=BASE_URL,
        rate_limiter=AsyncRateLimiter(max_per_minute=100, max_concurrent=10),
    )


@respx.mock
@pytest.mark.asyncio
async def test_fetch_profile_success(client: SelanetClient, profile_response: dict):
    respx.post(f"{BASE_URL}/api/rpc/scrapeUrl").mock(
        return_value=httpx.Response(200, json=profile_response)
    )
    result = await client.fetch_profile("testuser")
    assert isinstance(result, list)
    assert len(result) == 3
    assert result[0]["username"] == "testuser"
    await client.close()


@respx.mock
@pytest.mark.asyncio
async def test_fetch_profile_strips_at(client: SelanetClient, profile_response: dict):
    route = respx.post(f"{BASE_URL}/api/rpc/scrapeUrl").mock(
        return_value=httpx.Response(200, json=profile_response)
    )
    await client.fetch_profile("@testuser")
    body = json.loads(route.calls[0].request.content)
    assert body["url"] == "https://x.com/testuser"
    await client.close()


@respx.mock
@pytest.mark.asyncio
async def test_fetch_profile_not_found(client: SelanetClient):
    respx.post(f"{BASE_URL}/api/rpc/scrapeUrl").mock(
        return_value=httpx.Response(200, json={
            "success": False,
            "data": {
                "function": "ScrapeComplete",
                "jobId": "job-x",
                "url": "https://x.com/noone",
                "scrapeType": "TWITTER_PROFILE",
                "result": {},
                "state": "failed",
                "status": "NOT_FOUND",
            },
        })
    )
    with pytest.raises(ProfileNotFoundError):
        await client.fetch_profile("noone")
    await client.close()


@respx.mock
@pytest.mark.asyncio
async def test_fetch_profile_auth_error(client: SelanetClient):
    respx.post(f"{BASE_URL}/api/rpc/scrapeUrl").mock(
        return_value=httpx.Response(401, json={"error": "Unauthorized"})
    )
    with pytest.raises(SelanetAuthError):
        await client.fetch_profile("testuser")
    await client.close()


@respx.mock
@pytest.mark.asyncio
async def test_fetch_posts_success(client: SelanetClient, posts_response: dict):
    respx.post(f"{BASE_URL}/api/rpc/scrapeUrl").mock(
        return_value=httpx.Response(200, json=posts_response)
    )
    result = await client.fetch_posts("testuser", post_count=100)
    assert isinstance(result, list)
    assert len(result) == 3
    await client.close()


