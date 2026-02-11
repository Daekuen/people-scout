from __future__ import annotations

import json
import logging
from typing import Any

from google import genai
from google.genai import types

from people_scout.analysis.prompt import build_system_instruction, build_user_prompt
from people_scout.errors import PeopleScoutError

logger = logging.getLogger(__name__)

MAX_ANALYSIS_RETRIES = 2


class AnalysisError(PeopleScoutError):
    """LLM 분석 실패."""

    def __init__(self, message: str = "Analysis failed", raw_data: dict[str, Any] | None = None):
        super().__init__(message)
        self.raw_data = raw_data


class GeminiAPIError(AnalysisError):
    """Gemini API 호출 실패."""


class ResponseParseError(AnalysisError):
    """Gemini 응답 파싱/검증 실패."""


_RESPONSE_SCHEMA = {
    "type": "OBJECT",
    "properties": {
        "summary": {"type": "STRING"},
        "recent_interests": {
            "type": "ARRAY",
            "items": {
                "type": "OBJECT",
                "properties": {
                    "topic": {"type": "STRING"},
                    "frequency": {"type": "STRING", "enum": ["high", "medium", "low"]},
                    "sentiment": {
                        "type": "STRING",
                        "enum": ["positive", "negative", "neutral", "mixed"],
                    },
                    "evidence": {"type": "STRING"},
                },
                "required": ["topic", "frequency", "sentiment", "evidence"],
            },
        },
        "communication_style": {
            "type": "OBJECT",
            "properties": {
                "tone": {
                    "type": "STRING",
                    "enum": [
                        "professional", "casual", "academic",
                        "humorous", "provocative", "inspirational",
                    ],
                },
                "tone_description": {"type": "STRING"},
                "post_frequency": {
                    "type": "STRING",
                    "enum": ["very_active", "active", "moderate", "occasional", "rare"],
                },
                "active_hours": {"type": "STRING"},
                "content_type_ratio": {
                    "type": "OBJECT",
                    "properties": {
                        "original": {"type": "INTEGER"},
                        "retweet": {"type": "INTEGER"},
                        "reply": {"type": "INTEGER"},
                        "quote": {"type": "INTEGER"},
                    },
                    "required": ["original", "retweet", "reply", "quote"],
                },
                "engagement_style": {"type": "STRING"},
                "language_mix": {"type": "ARRAY", "items": {"type": "STRING"}},
            },
            "required": [
                "tone", "tone_description", "post_frequency", "active_hours",
                "content_type_ratio", "engagement_style", "language_mix",
            ],
        },
        "conversation_entry_points": {
            "type": "ARRAY",
            "items": {
                "type": "OBJECT",
                "properties": {
                    "topic": {"type": "STRING"},
                    "reason": {"type": "STRING"},
                    "suggested_approach": {"type": "STRING"},
                    "confidence": {"type": "STRING", "enum": ["high", "medium", "low"]},
                },
                "required": ["topic", "reason", "suggested_approach", "confidence"],
            },
        },
    },
    "required": [
        "summary", "recent_interests", "communication_style", "conversation_entry_points",
    ],
}


class GeminiAnalyzer:
    """Gemini 2.5 Flash 기반 인물 분석기."""

    def __init__(self, api_key: str, model: str = "gemini-2.5-flash"):
        self._client = genai.Client(api_key=api_key)
        self._model = model

    async def analyze_person(
        self,
        profile: dict[str, Any],
        posts: dict[str, Any] | None = None,
        lang: str = "ko",
    ) -> dict[str, Any]:
        """수집된 데이터를 분석하여 LLM 결과를 dict로 반환한다."""
        system_instruction = build_system_instruction(lang)
        user_prompt = build_user_prompt(profile, posts)

        for attempt in range(MAX_ANALYSIS_RETRIES):
            try:
                response = await self._client.aio.models.generate_content(
                    model=self._model,
                    contents=user_prompt,
                    config=types.GenerateContentConfig(
                        system_instruction=system_instruction,
                        response_mime_type="application/json",
                        response_schema=_RESPONSE_SCHEMA,
                        temperature=0.3,
                        max_output_tokens=8192,
                    ),
                )

                result = json.loads(response.text)
                return result

            except Exception as e:
                logger.warning(f"Analysis attempt {attempt + 1} failed: {e}")
                if attempt == MAX_ANALYSIS_RETRIES - 1:
                    raise GeminiAPIError(
                        message=f"Gemini API failed after {MAX_ANALYSIS_RETRIES} attempts: {e}",
                        raw_data={"profile": profile, "posts": posts},
                    ) from e

        raise GeminiAPIError("Unexpected analysis failure")
