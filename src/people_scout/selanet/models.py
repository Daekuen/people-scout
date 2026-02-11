from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel, Field


class ScrapeRequest(BaseModel):
    """Selanet API 스크래핑 요청."""

    url: str = Field(description="스크래핑 대상 URL")
    scrape_type: Literal[
        "TWITTER_PROFILE", "TWITTER_POST", "TWITTER_FOLLOW_LIST", "GOOGLE_SEARCH"
    ] = Field(alias="scrapeType")
    timeout_ms: int = Field(default=60000, alias="timeoutMs")
    post_count: int | None = Field(default=None, alias="postCount")

    model_config = {"populate_by_name": True}


class ScrapeData(BaseModel):
    """Selanet API 응답 data 필드."""

    function: str
    job_id: str = Field(alias="jobId")
    url: str
    scrape_type: str = Field(alias="scrapeType")
    result: dict[str, Any] | list[Any]
    state: str
    status: str

    model_config = {"populate_by_name": True}


class ScrapeResponse(BaseModel):
    """Selanet API 최상위 응답."""

    success: bool
    data: ScrapeData
