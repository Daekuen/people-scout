from __future__ import annotations

from people_scout.errors import PeopleScoutError


class SelanetError(PeopleScoutError):
    """Selanet API 관련 예외."""


class SelanetAuthError(SelanetError):
    """Selanet API 인증 실패 (401)."""


class SelanetRateLimitError(SelanetError):
    """Selanet API Rate Limit 초과 (429)."""

    def __init__(self, retry_after: float = 0.0, message: str = "Rate limit exceeded"):
        super().__init__(message)
        self.retry_after = retry_after


class SelanetTimeoutError(SelanetError):
    """Selanet API 요청 타임아웃."""


class SelanetScrapeError(SelanetError):
    """스크래핑 실패 (success: false)."""

    def __init__(self, scrape_type: str, message: str = "Scrape failed"):
        super().__init__(message)
        self.scrape_type = scrape_type


class ProfileNotFoundError(SelanetScrapeError):
    """프로필을 찾을 수 없음."""

    def __init__(self, handle: str):
        super().__init__(
            scrape_type="TWITTER_PROFILE",
            message=f"Profile not found: {handle}",
        )
        self.handle = handle
