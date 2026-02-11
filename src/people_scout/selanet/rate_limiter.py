from __future__ import annotations

import asyncio
import time


class AsyncRateLimiter:
    """asyncio 기반 토큰 버킷 Rate Limiter.

    Selanet API 제한: 분당 5회, 동시 5개.
    """

    def __init__(
        self,
        max_per_minute: int = 5,
        max_concurrent: int = 5,
    ):
        self._max_per_minute = max_per_minute
        self._max_concurrent = max_concurrent
        self._semaphore = asyncio.Semaphore(max_concurrent)
        self._timestamps: list[float] = []
        self._lock = asyncio.Lock()

    async def acquire(self) -> None:
        """토큰을 획득한다. 필요하면 Rate Limit까지 대기."""
        await self._semaphore.acquire()
        async with self._lock:
            now = time.monotonic()
            # 1분 이전 타임스탬프 제거
            self._timestamps = [t for t in self._timestamps if now - t < 60.0]

            if len(self._timestamps) >= self._max_per_minute:
                oldest = self._timestamps[0]
                wait_time = 60.0 - (now - oldest)
                if wait_time > 0:
                    await asyncio.sleep(wait_time)
                    now = time.monotonic()
                    self._timestamps = [t for t in self._timestamps if now - t < 60.0]

            self._timestamps.append(now)

    def release(self) -> None:
        """동시 실행 슬롯을 반환한다."""
        self._semaphore.release()

    async def __aenter__(self) -> AsyncRateLimiter:
        await self.acquire()
        return self

    async def __aexit__(self, *exc: object) -> None:
        self.release()
