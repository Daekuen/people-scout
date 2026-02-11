from __future__ import annotations

import asyncio
import logging
import time
from datetime import datetime, timezone
from typing import Any

from people_scout.analysis.analyzer import GeminiAnalyzer
from people_scout.analysis.models import PersonReport
from people_scout.config import ScoutSettings
from people_scout.selanet.client import SelanetClient
from people_scout.selanet.errors import SelanetScrapeError

logger = logging.getLogger(__name__)


class PeopleScout:
    """People Scout 메인 클래스.

    트위터 핸들을 분석하여 인물 인텔리전스 리포트를 생성한다.
    """

    def __init__(
        self,
        selanet_api_key: str | None = None,
        gemini_api_key: str | None = None,
        selanet_base_url: str | None = None,
        gemini_model: str | None = None,
    ):
        settings = ScoutSettings(
            selanet_api_key=selanet_api_key or "",
            selanet_base_url=selanet_base_url or "",
            gemini_api_key=gemini_api_key or "",
        ) if any([selanet_api_key, gemini_api_key, selanet_base_url]) else ScoutSettings()

        self._selanet = SelanetClient(
            api_key=settings.selanet_api_key,
            base_url=settings.selanet_base_url,
        )
        self._analyzer = GeminiAnalyzer(
            api_key=settings.gemini_api_key,
            model=gemini_model or settings.scout_gemini_model,
        )
        self._default_lang = settings.scout_default_lang

    def analyze(
        self,
        handle: str,
        *,
        lang: str | None = None,
        post_count: int = 100,
    ) -> PersonReport:
        """동기 분석 실행."""
        return asyncio.run(
            self.analyze_async(handle, lang=lang, post_count=post_count)
        )

    async def analyze_async(
        self,
        handle: str,
        *,
        lang: str | None = None,
        post_count: int = 100,
        on_progress: Any = None,
    ) -> PersonReport:
        """비동기 분석 실행."""
        lang = lang or self._default_lang
        handle_clean = handle.lstrip("@")
        start_time = time.monotonic()
        api_calls = 0

        try:
            # 1. TWITTER_PROFILE 수집 (필수)
            if on_progress:
                on_progress("profile", "start")
            profile_tweets = await self._selanet.fetch_profile(handle_clean)
            api_calls += 1
            if on_progress:
                on_progress("profile", "done")

            # 2. TWITTER_POST 수집 (추가 트윗, 실패 시 경고 + 계속)
            extra_tweets: list[dict[str, Any]] = []
            if on_progress:
                on_progress("posts", "start")
            try:
                extra_tweets = await self._selanet.fetch_posts(handle_clean, post_count=post_count)
                api_calls += 1
            except SelanetScrapeError as e:
                logger.warning(f"포스트 수집 실패, TWITTER_PROFILE 데이터만으로 분석 계속: {e}")
            if on_progress:
                on_progress("posts", "done")

            # 트윗 병합 (중복 제거)
            seen_ids = set()
            all_tweets: list[dict[str, Any]] = []
            for tweet in profile_tweets + extra_tweets:
                tid = tweet.get("tweetId")
                if tid and tid not in seen_ids:
                    seen_ids.add(tid)
                    all_tweets.append(tweet)
                elif not tid:
                    all_tweets.append(tweet)

            # 3. Gemini 분석
            if on_progress:
                on_progress("analysis", "start")

            username = handle_clean
            if all_tweets:
                username = all_tweets[0].get("username", handle_clean)

            analysis_result = await self._analyzer.analyze_person(
                profile={"handle": username},
                posts={"posts": all_tweets},
                lang=lang,
            )
            if on_progress:
                on_progress("analysis", "done")

            # 4. PersonReport 조합
            duration = time.monotonic() - start_time
            report = PersonReport(
                handle=f"@{handle_clean}",
                display_name=username,
                bio="",
                summary=analysis_result["summary"],
                recent_interests=analysis_result["recent_interests"],
                communication_style=analysis_result["communication_style"],
                conversation_entry_points=analysis_result["conversation_entry_points"],
                collected_at=datetime.now(timezone.utc),
                post_count=len(all_tweets),
                api_calls=api_calls,
                duration_seconds=round(duration, 1),
            )
            return report

        finally:
            await self._selanet.close()
