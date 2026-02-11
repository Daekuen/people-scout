from __future__ import annotations

import asyncio
import time

import pytest

from people_scout.selanet.rate_limiter import AsyncRateLimiter


@pytest.mark.asyncio
async def test_limiter_allows_within_limit():
    limiter = AsyncRateLimiter(max_per_minute=5, max_concurrent=5)
    for _ in range(5):
        async with limiter:
            pass  # 5회까지는 즉시 통과


@pytest.mark.asyncio
async def test_limiter_concurrent_limit():
    limiter = AsyncRateLimiter(max_per_minute=100, max_concurrent=2)
    active = 0
    max_active = 0

    async def task():
        nonlocal active, max_active
        async with limiter:
            active += 1
            max_active = max(max_active, active)
            await asyncio.sleep(0.05)
            active -= 1

    await asyncio.gather(*[task() for _ in range(5)])
    assert max_active <= 2


@pytest.mark.asyncio
async def test_limiter_context_manager():
    limiter = AsyncRateLimiter(max_per_minute=10, max_concurrent=5)
    async with limiter:
        pass  # 정상 동작 확인
