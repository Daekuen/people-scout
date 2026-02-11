from __future__ import annotations

from datetime import datetime
from pathlib import Path
from typing import Literal

from pydantic import BaseModel, Field


class ContentTypeRatio(BaseModel):
    """포스트 유형별 비율."""

    original: int = Field(ge=0, le=100, description="오리지널 포스트 비율 (%)")
    retweet: int = Field(ge=0, le=100, description="리트윗 비율 (%)")
    reply: int = Field(ge=0, le=100, description="댓글/답글 비율 (%)")
    quote: int = Field(ge=0, le=100, description="인용 트윗 비율 (%)")


class InterestItem(BaseModel):
    """개별 관심사 항목."""

    topic: str = Field(description="관심 주제")
    frequency: Literal["high", "medium", "low"] = Field(description="언급 빈도")
    sentiment: Literal["positive", "negative", "neutral", "mixed"] = Field(description="감성")
    evidence: str = Field(description="근거 요약 (1-2문장)")


class CommunicationStyle(BaseModel):
    """소통 스타일 분석 결과."""

    tone: Literal[
        "professional", "casual", "academic", "humorous", "provocative", "inspirational"
    ] = Field(description="주요 소통 톤")
    tone_description: str = Field(description="소통 톤 구체적 설명")
    post_frequency: Literal[
        "very_active", "active", "moderate", "occasional", "rare"
    ] = Field(description="포스팅 빈도")
    active_hours: str = Field(description="주요 활동 시간대")
    content_type_ratio: ContentTypeRatio = Field(description="포스트 유형별 비율")
    engagement_style: str = Field(description="상호작용 스타일 설명")
    language_mix: list[str] = Field(description="사용 언어 목록")


class ConversationEntry(BaseModel):
    """대화 시작을 위한 추천 주제/질문."""

    topic: str = Field(description="대화 주제")
    reason: str = Field(description="추천 이유")
    suggested_approach: str = Field(description="대화 접근 방법 제안")
    confidence: Literal["high", "medium", "low"] = Field(description="적절성 신뢰도")


class PersonReport(BaseModel):
    """인물 인텔리전스 리포트 최상위 모델."""

    # 기본 프로필
    handle: str = Field(description="트위터 핸들 (@포함)")
    display_name: str = Field(description="표시 이름")
    bio: str = Field(description="프로필 바이오")

    # LLM 분석 결과
    summary: str = Field(description="인물 2-3줄 종합 요약")
    recent_interests: list[InterestItem] = Field(description="최근 관심사 (최대 10개)")
    communication_style: CommunicationStyle = Field(description="소통 스타일")
    conversation_entry_points: list[ConversationEntry] = Field(description="대화 진입점 (3-5개)")

    # 메타데이터
    collected_at: datetime = Field(description="수집 시각 (UTC)")
    post_count: int = Field(description="분석에 사용된 포스트 수")
    api_calls: int = Field(description="API 호출 횟수")
    duration_seconds: float = Field(description="소요 시간 (초)")

    def to_json(self, path: str | Path) -> None:
        """JSON 파일로 저장."""
        Path(path).write_text(self.model_dump_json(indent=2), encoding="utf-8")

    def to_markdown(self, path: str | Path) -> None:
        """마크다운 리포트 파일로 저장."""
        from people_scout.output.markdown import render_markdown

        Path(path).write_text(render_markdown(self), encoding="utf-8")
