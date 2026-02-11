from __future__ import annotations

import asyncio
import logging
from typing import Any

import httpx

from people_scout.selanet.errors import (
    ProfileNotFoundError,
    SelanetAuthError,
    SelanetRateLimitError,
    SelanetScrapeError,
    SelanetTimeoutError,
)
from people_scout.selanet.models import ScrapeResponse
from people_scout.selanet.rate_limiter import AsyncRateLimiter

logger = logging.getLogger(__name__)

MAX_RETRIES = 3
INITIAL_BACKOFF = 2.0
BACKOFF_MULTIPLIER = 2.0
REQUEST_TIMEOUT = 120.0


class SelanetClient:
    """Selanet API HTTP 클라이언트."""

    def __init__(
        self,
        api_key: str,
        base_url: str,
        rate_limiter: AsyncRateLimiter | None = None,
    ):
        self._api_key = api_key
        self._base_url = base_url.rstrip("/")
        self._rate_limiter = rate_limiter or AsyncRateLimiter()
        self._client: httpx.AsyncClient | None = None

    async def _get_client(self) -> httpx.AsyncClient:
        if self._client is None or self._client.is_closed:
            self._client = httpx.AsyncClient(
                base_url=self._base_url,
                headers={
                    "Authorization": f"Bearer {self._api_key}",
                    "Content-Type": "application/json",
                },
                timeout=httpx.Timeout(REQUEST_TIMEOUT),
            )
        return self._client

    async def _request(self, payload: dict[str, Any]) -> ScrapeResponse:
        """Rate Limit + 재시도 적용된 API 요청."""
        last_error: Exception | None = None

        for attempt in range(MAX_RETRIES):
            async with self._rate_limiter:
                try:
                    client = await self._get_client()
                    response = await client.post("/api/rpc/scrapeUrl", json=payload)

                    if response.status_code == 401:
                        raise SelanetAuthError("Invalid API key")

                    if response.status_code == 429:
                        retry_after = float(response.headers.get("Retry-After", "10"))
                        raise SelanetRateLimitError(retry_after=retry_after)

                    response.raise_for_status()
                    return ScrapeResponse.model_validate(response.json())

                except SelanetAuthError:
                    raise
                except SelanetRateLimitError as e:
                    last_error = e
                    wait = e.retry_after if e.retry_after > 0 else INITIAL_BACKOFF * (BACKOFF_MULTIPLIER ** attempt)
                    logger.warning(f"Rate limited, waiting {wait:.1f}s (attempt {attempt + 1}/{MAX_RETRIES})")
                    await asyncio.sleep(wait)
                except httpx.TimeoutException as e:
                    last_error = SelanetTimeoutError(str(e))
                    if attempt < MAX_RETRIES - 1:
                        wait = INITIAL_BACKOFF * (BACKOFF_MULTIPLIER ** attempt)
                        logger.warning(f"Timeout, retrying in {wait:.1f}s (attempt {attempt + 1}/{MAX_RETRIES})")
                        await asyncio.sleep(wait)
                except httpx.HTTPStatusError as e:
                    last_error = e
                    if e.response.status_code >= 500 and attempt < MAX_RETRIES - 1:
                        wait = INITIAL_BACKOFF * (BACKOFF_MULTIPLIER ** attempt)
                        logger.warning(f"Server error {e.response.status_code}, retrying in {wait:.1f}s")
                        await asyncio.sleep(wait)
                    else:
                        raise

        raise last_error  # type: ignore[misc]

    def _extract_tweets(self, result: dict[str, Any] | list[Any]) -> list[dict[str, Any]]:
        """API result에서 트윗 리스트를 추출한다.

        실제 API 응답 형식:
        - TWITTER_PROFILE: list[tweet]
        - TWITTER_POST: {post: {}, reply: [tweet]}
        """
        if isinstance(result, list):
            return result
        if isinstance(result, dict):
            # TWITTER_POST 형식: reply 필드에 트윗 목록
            if "reply" in result and isinstance(result["reply"], list):
                return result["reply"]
            if "posts" in result and isinstance(result["posts"], list):
                return result["posts"]
        return []

    async def fetch_profile(self, handle: str) -> list[dict[str, Any]]:
        """트위터 프로필 트윗을 수집한다.

        TWITTER_PROFILE은 최근 트윗 리스트를 반환한다.
        프로필 메타데이터(bio, 팔로워 수)는 포함되지 않는다.
        """
        handle = handle.lstrip("@")
        resp = await self._request({
            "url": f"https://x.com/{handle}",
            "scrapeType": "TWITTER_PROFILE",
            "timeoutMs": 60000,
        })
        if not resp.success:
            raise ProfileNotFoundError(handle)
        tweets = self._extract_tweets(resp.data.result)
        if not tweets:
            raise ProfileNotFoundError(handle)
        return tweets

    async def fetch_posts(self, handle: str, post_count: int = 100) -> list[dict[str, Any]]:
        """트위터 포스트를 수집한다."""
        handle = handle.lstrip("@")
        resp = await self._request({
            "url": f"https://x.com/{handle}",
            "scrapeType": "TWITTER_POST",
            "timeoutMs": 60000,
            "postCount": post_count,
        })
        if not resp.success:
            raise SelanetScrapeError("TWITTER_POST", f"Failed to fetch posts for @{handle}")
        return self._extract_tweets(resp.data.result)

    async def close(self) -> None:
        if self._client and not self._client.is_closed:
            await self._client.aclose()
