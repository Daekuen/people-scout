# People Scout - Product Requirements Document (PRD)

## 문서 정보

| 항목 | 내용 |
|------|------|
| 제품명 | People Scout |
| 버전 | 0.1.0 |
| 작성일 | 2026-02-12 |
| 상태 | 개발 중 |
| 카테고리 | SOCIAL MEDIA (Selanet AI Agent Marketplace) |

---

## 1. 개요

### 1.1 제품 정의

People Scout는 트위터(X) 핸들 하나를 입력하면 해당 인물에 대한 인텔리전스 리포트를 자동 생성하는 AI 에이전트이다. Selanet API로 트위터 데이터(프로필, 포스트, 팔로우 리스트)를 수집하고, Gemini 2.5 Flash로 분석하여 구조화된 리포트를 출력한다.

### 1.2 핵심 가치

| 가치 | 설명 |
|------|------|
| **원클릭 인사이트** | 핸들 하나만 입력하면 인물 분석 리포트 자동 생성 |
| **대화 준비** | 미팅 전 상대방의 관심사, 소통 스타일, 대화 진입점 파악 |
| **네트워크 파악** | deep 모드로 인맥 구조와 영향력 분석 |
| **다국어 지원** | 한국어/영어 리포트 생성 |

### 1.3 제품 한 줄 요약

> "트위터 핸들 하나로 인물 인텔리전스 리포트를 자동 생성하는 AI 에이전트"

---

## 2. 목표 사용자

### 2.1 페르소나

#### 페르소나 1: 비즈니스 개발 담당자 (BD Manager)

| 항목 | 내용 |
|------|------|
| 이름 | 김민수 (가상) |
| 직무 | BD / 파트너십 매니저 |
| 경험 | 5년차, 주 3-5회 외부 미팅 |
| 핵심 니즈 | 미팅 상대방의 최근 관심사와 대화 진입점을 빠르게 파악 |
| 페인 포인트 | 미팅 전 상대방 SNS를 일일이 훑어보는 데 30분 이상 소요 |
| 기대 결과 | 5분 안에 상대방 분석 리포트 확보 |

#### 페르소나 2: 투자자 / VC

| 항목 | 내용 |
|------|------|
| 이름 | 이지현 (가상) |
| 직무 | VC 심사역 |
| 경험 | 7년차, 주 10건 이상 딜 소싱 |
| 핵심 니즈 | 창업자의 관심 분야, 네트워크, 영향력 빠르게 파악 |
| 페인 포인트 | 여러 소스를 교차 확인하는 데 시간 소모 |
| 기대 결과 | 창업자 인물 리포트 + 네트워크 인사이트 |

#### 페르소나 3: 개발자 / 자동화 구축자

| 항목 | 내용 |
|------|------|
| 이름 | 박서준 (가상) |
| 직무 | 백엔드 개발자 |
| 경험 | 3년차, 사이드 프로젝트 활발 |
| 핵심 니즈 | SDK/API로 인물 분석을 자신의 워크플로우에 통합 |
| 페인 포인트 | 트위터 API 직접 다루기 복잡, 분석 로직 직접 구현 부담 |
| 기대 결과 | `pip install` 후 3줄 코드로 분석 결과 획득 |

### 2.2 유저 스토리

#### US-1: 기본 인물 분석

```
As a 비즈니스 개발 담당자
I want to 트위터 핸들을 입력하면 인물 분석 리포트를 받고 싶다
So that 미팅 전 상대방을 빠르게 파악할 수 있다
```

**수용 조건:**
- Given 유효한 트위터 핸들 `@handle`
- When `people-scout @handle` 실행
- Then 프로필 요약, 최근 관심사, 소통 스타일, 대화 진입점이 포함된 리포트 출력

#### US-2: 딥 분석 (네트워크 포함)

```
As a 투자자
I want to 인물의 팔로우 리스트까지 분석한 deep 리포트를 받고 싶다
So that 해당 인물의 네트워크와 영향력을 파악할 수 있다
```

**수용 조건:**
- Given 유효한 트위터 핸들과 `--deep` 옵션
- When `people-scout @handle --deep` 실행
- Then 기본 리포트 + 네트워크 인사이트(주요 연결, 클러스터, 영향력 지표) 포함

#### US-3: SDK 통합

```
As a 개발자
I want to Python SDK로 인물 분석을 내 애플리케이션에 통합하고 싶다
So that 자동화된 워크플로우를 구축할 수 있다
```

**수용 조건:**
- Given `pip install people-scout` 완료
- When `PeopleScout(...).analyze("@handle")` 호출
- Then `PersonReport` Pydantic 모델 객체 반환

#### US-4: 다양한 출력 형식

```
As a 사용자
I want to 분석 결과를 콘솔, JSON, 마크다운 등 다양한 형식으로 받고 싶다
So that 용도에 맞게 리포트를 활용할 수 있다
```

**수용 조건:**
- Given 분석 완료된 `PersonReport`
- When `--output console,json,markdown` 지정
- Then 터미널 출력 + `report.json` + `report.md` 동시 생성

#### US-5: 다국어 리포트

```
As a 한국어 사용자
I want to 리포트를 한국어로 받고 싶다
So that 한국어로 바로 활용할 수 있다
```

**수용 조건:**
- Given `--lang ko` 옵션 또는 `lang="ko"` 파라미터
- When 분석 실행
- Then 리포트의 모든 분석 텍스트가 한국어로 출력

---

## 3. 범위

### 3.1 In-Scope (v0.1.0)

| 기능 | 설명 |
|------|------|
| 프로필 수집 | Selanet API로 트위터 프로필 수집 |
| 포스트 수집 | 최근 100개 포스트 수집 |
| 팔로우 수집 | deep 모드에서 팔로우/팔로워 리스트 수집 |
| LLM 분석 | Gemini 2.5 Flash로 수집 데이터 분석 |
| 구조화된 리포트 | PersonReport 모델로 결과 반환 |
| CLI | `people-scout @handle` 커맨드 |
| SDK | Python SDK (`PeopleScout` 클래스) |
| 출력 포맷 | 콘솔 (Rich), JSON, 마크다운 |
| 다국어 | 한국어, 영어 |
| Rate Limiting | Selanet API 분당 5회 제한 준수 |
| 에러 핸들링 | Graceful degradation 전략 |

### 3.2 Out-of-Scope (v0.1.0)

| 항목 | 이유 |
|------|------|
| 웹 UI | CLI/SDK 우선, 추후 별도 프로젝트 |
| 데이터 캐싱 | 첫 버전은 매번 실시간 수집 |
| 배치 분석 | 단일 핸들 분석 우선 |
| 히스토리 비교 | 시간별 변화 추적은 추후 |
| 다른 SNS 지원 | 트위터(X) 전용 |
| 인증/과금 | 사용자가 직접 API 키 관리 |

---

## 4. 핵심 기능

### 4.1 Epic 1: 트위터 데이터 수집

#### Story 1.1: 프로필 수집

- Selanet API `TWITTER_PROFILE` scrapeType으로 프로필 데이터 수집
- 수집 항목: display_name, bio, followers_count, following_count, post_count, join_date, location, website, verified 여부
- 프로필 수집 실패 시 전체 분석 중단 (치명적 에러)

#### Story 1.2: 포스트 수집

- Selanet API `TWITTER_POST` scrapeType으로 최근 포스트 수집
- `postCount: 100` (기본값)
- 수집 항목: 텍스트, 작성일, 좋아요/리트윗/댓글 수, 미디어 여부, 인용 여부
- 포스트 수집 실패 시 경고 + 프로필만으로 분석 계속

#### Story 1.3: 팔로우 리스트 수집 (deep 모드)

- `--deep` 옵션 활성화 시에만 실행
- Selanet API `TWITTER_FOLLOW_LIST` scrapeType 사용
- 수집 항목: 팔로우/팔로워 핸들 목록, 프로필 요약
- 팔로우 수집 실패 시 경고 + 네트워크 분석 스킵

#### Story 1.4: Rate Limiter

- Selanet API 제한: 분당 5회, 동시 5개, 타임아웃 10분
- asyncio 기반 토큰 버킷 또는 슬라이딩 윈도우 방식
- 429 응답 시 자동 대기 후 재시도 (exponential backoff)
- 최대 재시도 횟수: 3회

### 4.2 Epic 2: LLM 분석

#### Story 2.1: Gemini 2.5 Flash 통합

- `google-genai` SDK 사용
- Structured Output으로 `PersonReport` Pydantic 모델 직접 반환
- 비동기 호출 지원 (`client.aio.models.generate_content`)

#### Story 2.2: 프롬프트 전략

- System Instruction으로 분석가 역할 정의
- 수집된 데이터를 구조화하여 프롬프트에 포함
- 언어 옵션(`lang`)에 따라 프롬프트 언어 분기
- 프롬프트 구성 상세는 [섹션 8. 프롬프트 전략](#8-프롬프트-전략) 참조

#### Story 2.3: 분석 결과 구조화

- Gemini의 `response_mime_type: "application/json"` + `response_schema` 활용
- Pydantic 모델로 응답 검증 및 파싱
- LLM 분석 실패 시 raw 데이터만으로 최소 리포트 생성

### 4.3 Epic 3: 출력 및 인터페이스

#### Story 3.1: CLI 인터페이스

- Click 기반 커맨드 라인 도구
- 커맨드: `people-scout <handle> [options]`
- 옵션:
  - `--deep`: 팔로우 리스트 포함 분석
  - `--lang [ko|en]`: 리포트 언어 (기본: ko)
  - `--output [console|json|markdown]`: 출력 형식 (쉼표 구분, 복수 선택 가능, 기본: console)
  - `--post-count N`: 수집할 포스트 수 (기본: 100)
  - `--output-dir PATH`: 파일 출력 디렉토리 (기본: 현재 디렉토리)

#### Story 3.2: 콘솔 출력

- Rich 라이브러리로 터미널에 리포트 렌더링
- 진행 상황 표시: 스피너 + 단계별 진행률
- 섹션별 구분: Panel, Table, 색상 구분

#### Story 3.3: JSON 출력

- `PersonReport.model_dump_json()` 기반
- 파일 저장: `{handle}_report.json`
- 프로그래밍 방식 활용 용이

#### Story 3.4: 마크다운 출력

- 구조화된 마크다운 리포트 생성
- 파일 저장: `{handle}_report.md`
- 섹션: 요약, 관심사 테이블, 소통 스타일, 대화 진입점, 네트워크 인사이트

#### Story 3.5: SDK 인터페이스

- `PeopleScout` 클래스로 프로그래밍 방식 접근
- `analyze()` 메서드: 동기 실행 (내부 asyncio.run)
- `analyze_async()` 메서드: 비동기 실행
- `PersonReport` 객체에 `to_json()`, `to_markdown()` 편의 메서드

---

## 5. 기술 스택

| 항목 | 선택 | 버전 | 용도 |
|------|------|------|------|
| Python | 3.11+ | >= 3.11 | 런타임 |
| httpx | httpx | >= 0.27.0 | Selanet API HTTP 클라이언트 (async 지원) |
| google-genai | google-genai | >= 1.0.0 | Gemini 2.5 Flash LLM API |
| click | click | >= 8.1.0 | CLI 프레임워크 |
| rich | rich | >= 13.0.0 | 터미널 출력 (테이블, 스피너, 패널) |
| pydantic | pydantic | >= 2.9.0 | 데이터 모델, 직렬화, 검증 |
| pydantic-settings | pydantic-settings | >= 2.6.0 | 환경변수 기반 설정 관리 |
| python-dotenv | python-dotenv | >= 1.0.0 | .env 파일 로딩 |
| pytest | pytest | >= 8.0.0 | 테스트 프레임워크 (dev) |
| pytest-asyncio | pytest-asyncio | >= 0.24.0 | 비동기 테스트 지원 (dev) |
| respx | respx | >= 0.22.0 | httpx 모킹 (dev) |
| ruff | ruff | >= 0.8.0 | 린터/포매터 (dev) |
| hatchling | hatchling | - | 빌드 백엔드 |

### 5.1 의존성 (pyproject.toml)

```toml
[project]
dependencies = [
    "httpx>=0.27.0",
    "google-genai>=1.0.0",
    "click>=8.1.0",
    "rich>=13.0.0",
    "pydantic>=2.9.0",
    "pydantic-settings>=2.6.0",
    "python-dotenv>=1.0.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=8.0.0",
    "pytest-asyncio>=0.24.0",
    "respx>=0.22.0",
    "ruff>=0.8.0",
]
```

### 5.2 환경변수

| 변수명 | 필수 | 설명 | 기본값 |
|--------|------|------|--------|
| `SELANET_API_KEY` | O | Selanet API 인증 키 | - |
| `SELANET_BASE_URL` | O | Selanet API 베이스 URL | - |
| `GEMINI_API_KEY` | O | Google Gemini API 키 | - |
| `SCOUT_GEMINI_MODEL` | X | 사용할 Gemini 모델 ID | `gemini-2.5-flash` |
| `SCOUT_DEFAULT_LANG` | X | 기본 리포트 언어 | `ko` |
| `SCOUT_LOG_LEVEL` | X | 로그 레벨 | `info` |

### 5.3 .env.example

```env
SELANET_API_KEY=your_selanet_api_key
SELANET_BASE_URL=https://your-selanet-server.com
GEMINI_API_KEY=your_gemini_api_key
SCOUT_GEMINI_MODEL=gemini-2.5-flash
SCOUT_DEFAULT_LANG=ko
SCOUT_LOG_LEVEL=info
```

---

## 6. 데이터 모델 (상세)

모든 모델은 `pydantic.BaseModel` 기반이며 `src/people_scout/analysis/models.py`에 정의한다.

### 6.1 PersonReport (최상위 리포트 모델)

```python
from datetime import datetime
from pydantic import BaseModel, Field


class PersonReport(BaseModel):
    """인물 인텔리전스 리포트 최상위 모델."""

    # 기본 프로필 정보
    handle: str = Field(description="트위터 핸들 (@포함)")
    display_name: str = Field(description="표시 이름")
    bio: str = Field(description="프로필 바이오")

    # LLM 분석 결과
    summary: str = Field(
        description="인물에 대한 2-3줄 종합 요약. "
        "직업적 포지션, 주요 활동 영역, 핵심 특징을 포함."
    )
    recent_interests: list[InterestItem] = Field(
        description="최근 포스트 기반 관심사 목록 (최대 10개, 빈도 내림차순)"
    )
    communication_style: CommunicationStyle = Field(
        description="소통 스타일 분석 결과"
    )
    conversation_entry_points: list[ConversationEntry] = Field(
        description="이 인물과 대화를 시작하기 위한 추천 주제/질문 (3-5개)"
    )
    network_insights: NetworkInsights | None = Field(
        default=None,
        description="인맥/네트워크 분석 결과. deep 모드에서만 제공."
    )

    # 메타데이터
    collected_at: datetime = Field(description="데이터 수집 시각 (UTC)")
    post_count: int = Field(description="분석에 사용된 포스트 수")
    api_calls: int = Field(description="Selanet API 호출 횟수")
    duration_seconds: float = Field(description="전체 분석 소요 시간 (초)")
```

### 6.2 InterestItem (관심사 항목)

```python
class InterestItem(BaseModel):
    """개별 관심사 항목."""

    topic: str = Field(
        description="관심 주제 (예: 'AI/ML', '스타트업 투자', 'Web3')"
    )
    frequency: Literal["high", "medium", "low"] = Field(
        description="해당 주제 언급 빈도. "
        "high: 포스트의 30% 이상, medium: 10-30%, low: 10% 미만"
    )
    sentiment: Literal["positive", "negative", "neutral", "mixed"] = Field(
        description="해당 주제에 대한 감성. "
        "positive: 긍정적/옹호, negative: 비판적, "
        "neutral: 중립적/정보 공유, mixed: 긍부정 혼재"
    )
    evidence: str = Field(
        description="해당 관심사를 뒷받침하는 근거 요약 (1-2문장). "
        "구체적인 포스트 내용이나 패턴 언급."
    )
```

### 6.3 CommunicationStyle (소통 스타일)

```python
class CommunicationStyle(BaseModel):
    """소통 스타일 분석 결과."""

    tone: Literal[
        "professional", "casual", "academic",
        "humorous", "provocative", "inspirational"
    ] = Field(
        description="주요 소통 톤. "
        "professional: 비즈니스/전문적, casual: 일상적/편안한, "
        "academic: 학술적/분석적, humorous: 유머러스, "
        "provocative: 도발적/논쟁적, inspirational: 영감/동기부여"
    )
    tone_description: str = Field(
        description="소통 톤에 대한 구체적 설명 (1-2문장)"
    )
    post_frequency: Literal["very_active", "active", "moderate", "occasional", "rare"] = Field(
        description="포스팅 빈도. "
        "very_active: 하루 5회 이상, active: 하루 1-5회, "
        "moderate: 주 3-5회, occasional: 주 1-2회, rare: 월 수회 이하"
    )
    active_hours: str = Field(
        description="주요 활동 시간대 설명 (예: '오전 9-11시, 저녁 8-10시 집중')"
    )
    content_type_ratio: ContentTypeRatio = Field(
        description="포스트 유형별 비율"
    )
    engagement_style: str = Field(
        description="다른 사용자와의 상호작용 스타일 설명 (1-2문장). "
        "리트윗/인용/댓글 패턴, 대화 참여 방식 등."
    )
    language_mix: list[str] = Field(
        description="사용 언어 목록 (예: ['Korean', 'English'])"
    )
```

### 6.4 ContentTypeRatio (포스트 유형 비율)

```python
class ContentTypeRatio(BaseModel):
    """포스트 유형별 비율."""

    original: int = Field(
        ge=0, le=100,
        description="오리지널 포스트 비율 (%, 0-100)"
    )
    retweet: int = Field(
        ge=0, le=100,
        description="리트윗 비율 (%, 0-100)"
    )
    reply: int = Field(
        ge=0, le=100,
        description="댓글/답글 비율 (%, 0-100)"
    )
    quote: int = Field(
        ge=0, le=100,
        description="인용 트윗 비율 (%, 0-100)"
    )
```

### 6.5 ConversationEntry (대화 진입점)

```python
class ConversationEntry(BaseModel):
    """대화 시작을 위한 추천 주제/질문."""

    topic: str = Field(
        description="대화 주제 (예: '최근 관심 있는 AI 스타트업')"
    )
    reason: str = Field(
        description="이 주제를 추천하는 이유 (1-2문장). "
        "최근 포스트나 활동 패턴 근거."
    )
    suggested_approach: str = Field(
        description="대화 접근 방법 제안 (1-2문장). "
        "구체적인 질문이나 화두 예시."
    )
    confidence: Literal["high", "medium", "low"] = Field(
        description="이 대화 주제의 적절성 신뢰도. "
        "high: 최근 자주/적극적으로 언급, "
        "medium: 간헐적 언급, low: 프로필/맥락 기반 추론"
    )
```

### 6.6 NetworkInsights (네트워크 인사이트, deep 모드 전용)

```python
class NetworkInsights(BaseModel):
    """인맥/네트워크 분석 결과. --deep 모드에서만 생성."""

    total_following: int = Field(description="팔로잉 수")
    total_followers: int = Field(description="팔로워 수")
    follower_following_ratio: float = Field(
        description="팔로워/팔로잉 비율. 1 이상이면 영향력 지표."
    )
    notable_connections: list[NotableConnection] = Field(
        description="주목할 만한 연결 (최대 10명). 영향력/관련성 순."
    )
    network_clusters: list[NetworkCluster] = Field(
        description="네트워크 클러스터 (최대 5개). "
        "팔로우 리스트에서 발견되는 그룹/커뮤니티."
    )
    influence_assessment: str = Field(
        description="영향력 종합 평가 (2-3문장). "
        "팔로워 수, 연결의 질, 네트워크 다양성 종합."
    )
```

### 6.7 NotableConnection (주목할 연결)

```python
class NotableConnection(BaseModel):
    """주목할 만한 네트워크 연결."""

    handle: str = Field(description="트위터 핸들")
    display_name: str = Field(description="표시 이름")
    relationship: Literal["mutual", "following", "follower"] = Field(
        description="관계 유형. mutual: 상호 팔로우, "
        "following: 이 인물이 팔로우, follower: 이 인물을 팔로우"
    )
    relevance: str = Field(
        description="관계의 의미/맥락 설명 (1문장). "
        "예: '같은 업계 CEO', 'AI 연구자 커뮤니티'"
    )
```

### 6.8 NetworkCluster (네트워크 클러스터)

```python
class NetworkCluster(BaseModel):
    """네트워크에서 발견된 그룹/커뮤니티."""

    name: str = Field(
        description="클러스터 이름 (예: 'AI/ML 연구자', 'VC/투자자', '크립토 커뮤니티')"
    )
    description: str = Field(
        description="클러스터 설명 (1-2문장)"
    )
    member_count: int = Field(
        description="해당 클러스터에 속하는 팔로우/팔로워 수 (추정)"
    )
    representative_handles: list[str] = Field(
        description="대표 핸들 목록 (최대 5개)"
    )
```

### 6.9 Selanet API 모델 (selanet/models.py)

```python
from typing import Literal, Any
from pydantic import BaseModel, Field


class ScrapeRequest(BaseModel):
    """Selanet API 스크래핑 요청."""

    url: str = Field(description="스크래핑 대상 URL")
    scrape_type: Literal[
        "TWITTER_PROFILE", "TWITTER_POST",
        "TWITTER_FOLLOW_LIST", "GOOGLE_SEARCH"
    ] = Field(alias="scrapeType", description="스크래핑 유형")
    timeout_ms: int = Field(
        default=60000, alias="timeoutMs",
        description="타임아웃 (밀리초)"
    )
    post_count: int | None = Field(
        default=None, alias="postCount",
        description="수집할 포스트 수 (TWITTER_POST에서만 사용)"
    )

    model_config = {"populate_by_name": True}


class ScrapeData(BaseModel):
    """Selanet API 응답 data 필드."""

    function: str
    job_id: str = Field(alias="jobId")
    url: str
    scrape_type: str = Field(alias="scrapeType")
    result: dict[str, Any]
    state: str
    status: str

    model_config = {"populate_by_name": True}


class ScrapeResponse(BaseModel):
    """Selanet API 최상위 응답."""

    success: bool
    data: ScrapeData
```

---

## 7. API 스펙

### 7.1 Selanet API (외부 의존)

```
POST {SELANET_BASE_URL}/api/rpc/scrapeUrl
Authorization: Bearer {SELANET_API_KEY}
Content-Type: application/json
```

#### 요청 본문

```json
{
  "url": "https://x.com/{handle}",
  "scrapeType": "TWITTER_PROFILE | TWITTER_POST | TWITTER_FOLLOW_LIST",
  "timeoutMs": 60000,
  "postCount": 100
}
```

#### 응답

```json
{
  "success": true,
  "data": {
    "function": "ScrapeComplete",
    "jobId": "uuid-string",
    "url": "https://x.com/{handle}",
    "scrapeType": "TWITTER_PROFILE",
    "result": { "...프로필/포스트/팔로우 데이터..." },
    "state": "completed",
    "status": "OK"
  }
}
```

#### Rate Limit

| 제한 | 값 |
|------|-----|
| 분당 요청 | 5회 |
| 동시 요청 | 5개 |
| 요청 타임아웃 | 10분 (600,000ms) |

#### 에러 응답

| HTTP 코드 | 의미 | 처리 |
|-----------|------|------|
| 200 + `success: false` | 스크래핑 실패 | scrapeType별 degradation 전략 |
| 401 | 인증 실패 | `SelanetAuthError` raise |
| 429 | Rate Limit 초과 | 자동 대기 + 재시도 |
| 500 | 서버 에러 | 재시도 (최대 3회) |
| timeout | 요청 타임아웃 | 재시도 (최대 2회) |

### 7.2 Gemini API (외부 의존)

```python
from google import genai
from google.genai import types

client = genai.Client(api_key=GEMINI_API_KEY)

response = client.models.generate_content(
    model="gemini-2.5-flash",  # SCOUT_GEMINI_MODEL
    contents=prompt_text,
    config=types.GenerateContentConfig(
        system_instruction=system_prompt,
        response_mime_type="application/json",
        response_schema=PersonReport,
        temperature=0.3,
        max_output_tokens=8192,
    ),
)

report = PersonReport.model_validate_json(response.text)
```

#### 비동기 호출

```python
response = await client.aio.models.generate_content(
    model="gemini-2.5-flash",
    contents=prompt_text,
    config=types.GenerateContentConfig(
        system_instruction=system_prompt,
        response_mime_type="application/json",
        response_schema=PersonReport,
        temperature=0.3,
        max_output_tokens=8192,
    ),
)
```

---

## 8. 프롬프트 전략

### 8.1 System Instruction

```text
You are an expert person intelligence analyst. Your job is to analyze
Twitter/X data about a person and produce a structured intelligence report.

Rules:
1. Base all analysis strictly on the provided data. Do not hallucinate.
2. When evidence is insufficient, say so explicitly rather than guessing.
3. For sentiment analysis, consider context and nuance.
4. For network analysis, identify meaningful patterns, not just counts.
5. Provide actionable conversation entry points based on concrete evidence.
6. Output language: {lang} (ko = Korean, en = English)
```

### 8.2 User Prompt 구조

프롬프트는 수집된 데이터를 아래 구조로 정리하여 전달한다.

```text
## Target Person
Handle: @{handle}
Display Name: {display_name}
Bio: {bio}
Followers: {followers_count} | Following: {following_count}
Join Date: {join_date}
Location: {location}

## Recent Posts ({post_count} posts)
{posts_formatted}

## Follow List (if deep mode)
### Following ({following_count} accounts)
{following_list_formatted}

### Followers ({follower_count} accounts)
{followers_list_formatted}

---

Analyze this person and generate a comprehensive intelligence report.
Focus on:
1. A concise 2-3 sentence summary of who this person is
2. Their recent interests with frequency and sentiment
3. Their communication style and patterns
4. Actionable conversation entry points
5. Network insights (if follow data provided)
```

### 8.3 포스트 포매팅

각 포스트를 다음 형식으로 정리:

```text
[{index}] {date} | Likes: {likes} | RTs: {retweets} | Replies: {replies}
{text}
---
```

### 8.4 Gemini 설정

| 파라미터 | 값 | 이유 |
|----------|-----|------|
| `temperature` | 0.3 | 분석 일관성 확보, 창의적 추론은 최소화 |
| `max_output_tokens` | 8192 | deep 모드 네트워크 분석 포함 시 충분한 공간 |
| `response_mime_type` | `application/json` | 구조화된 JSON 출력 강제 |
| `response_schema` | `PersonReport` | Pydantic 모델 기반 스키마 검증 |

### 8.5 다국어 전략

- `lang="ko"`: System Instruction에 `Output language: Korean` 명시
- `lang="en"`: System Instruction에 `Output language: English` 명시
- 분석 대상 포스트가 다른 언어여도, 리포트는 지정 언어로 출력
- 고유명사, 기술 용어는 원어 병기 허용

---

## 9. CLI / SDK 인터페이스

### 9.1 CLI 인터페이스

```bash
# 기본 사용
people-scout @handle

# 전체 옵션
people-scout @handle \
  --deep \
  --lang ko \
  --output console,json,markdown \
  --post-count 100 \
  --output-dir ./reports
```

#### CLI 옵션 상세

| 옵션 | 축약 | 타입 | 기본값 | 설명 |
|------|------|------|--------|------|
| `handle` | - | argument | (필수) | 분석 대상 트위터 핸들 (@포함 또는 미포함) |
| `--deep` | `-d` | flag | False | 팔로우 리스트 포함 deep 분석 |
| `--lang` | `-l` | choice | ko | 리포트 언어 (ko, en) |
| `--output` | `-o` | string | console | 출력 형식 (쉼표 구분: console, json, markdown) |
| `--post-count` | `-p` | int | 100 | 수집할 포스트 수 |
| `--output-dir` | | path | . | 파일 출력 디렉토리 |

#### CLI 출력 예시

```
$ people-scout @kimceo --deep --lang ko

 People Scout v0.1.0

 [1/3] 프로필 수집 중... done
 [2/3] 포스트 수집 중 (100개)... done
 [3/3] 팔로우 리스트 수집 중... done

 Gemini 분석 중...

 ── 인물 리포트: 김대표 (@kimceo) ────────────────────

 요약
 AI 스타트업 대표로 B2B SaaS와 생성형 AI에 깊은 관심을 가진 기업가.
 한국 스타트업 생태계에서 활발히 네트워킹하며 투자 유치 경험을 공유한다.

 최근 관심사
 ┌──────────────────┬────────┬──────────┐
 │ 주제             │ 빈도   │ 감성     │
 ├──────────────────┼────────┼──────────┤
 │ 생성형 AI        │ high   │ positive │
 │ B2B SaaS         │ high   │ positive │
 │ 스타트업 투자    │ medium │ mixed    │
 │ ...              │ ...    │ ...      │
 └──────────────────┴────────┴──────────┘

 소통 스타일
 톤: professional | 빈도: active | 언어: Korean, English

 대화 진입점
 1. 최근 관심 있는 AI 스타트업 (신뢰도: high)
    "최근 생성형 AI를 제품에 어떻게 적용하고 계신가요?"
 2. ...

 네트워크 인사이트
 팔로잉: 1,234 | 팔로워: 5,678 | 비율: 4.6x
 ...

 완료 (12.3초, API 3회)
```

### 9.2 SDK 인터페이스

#### 초기화

```python
from people_scout import PeopleScout

# 방법 1: 직접 키 전달
scout = PeopleScout(
    selanet_api_key="sk-...",
    gemini_api_key="AIza...",
    selanet_base_url="https://...",
)

# 방법 2: 환경변수에서 자동 로딩 (.env 지원)
scout = PeopleScout()
```

#### 분석 실행

```python
# 기본 분석
result = scout.analyze("@kimceo")

# deep 분석 + 영어 리포트
result = scout.analyze("@kimceo", deep=True, lang="en")

# 비동기 실행
result = await scout.analyze_async("@kimceo", deep=True, lang="ko")
```

#### 결과 활용

```python
# 개별 필드 접근
print(result.summary)
print(result.recent_interests)
print(result.communication_style.tone)
print(result.conversation_entry_points[0].suggested_approach)

if result.network_insights:
    print(result.network_insights.influence_assessment)

# 파일 출력
result.to_json("report.json")
result.to_markdown("report.md")

# dict/JSON 변환
data = result.model_dump()
json_str = result.model_dump_json(indent=2)
```

#### analyze() 시그니처

```python
def analyze(
    self,
    handle: str,
    *,
    deep: bool = False,
    lang: str = "ko",
    post_count: int = 100,
) -> PersonReport:
    """
    트위터 핸들을 분석하여 인물 인텔리전스 리포트를 생성한다.

    Args:
        handle: 트위터 핸들 (@포함 또는 미포함)
        deep: True면 팔로우 리스트까지 수집하여 네트워크 분석 포함
        lang: 리포트 언어 ("ko" 또는 "en")
        post_count: 수집할 포스트 수 (기본 100)

    Returns:
        PersonReport: 구조화된 인물 분석 리포트

    Raises:
        SelanetAuthError: API 키 인증 실패
        ProfileNotFoundError: 프로필을 찾을 수 없음
        AnalysisError: LLM 분석 실패 (raw 데이터 포함)
    """
```

---

## 10. 에러 핸들링

### 10.1 에러 계층 구조

```python
# errors.py (기본)
class PeopleScoutError(Exception):
    """People Scout 기본 예외."""
    pass

class ConfigError(PeopleScoutError):
    """설정 오류 (환경변수 누락 등)."""
    pass

# selanet/errors.py
class SelanetError(PeopleScoutError):
    """Selanet API 관련 예외."""
    pass

class SelanetAuthError(SelanetError):
    """Selanet API 인증 실패 (401)."""
    pass

class SelanetRateLimitError(SelanetError):
    """Selanet API Rate Limit 초과 (429)."""
    retry_after: float  # 재시도까지 대기 시간 (초)

class SelanetTimeoutError(SelanetError):
    """Selanet API 요청 타임아웃."""
    pass

class SelanetScrapeError(SelanetError):
    """스크래핑 실패 (success: false)."""
    scrape_type: str
    pass

class ProfileNotFoundError(SelanetScrapeError):
    """프로필을 찾을 수 없음."""
    pass

# analysis 관련
class AnalysisError(PeopleScoutError):
    """LLM 분석 실패."""
    raw_data: dict | None  # 수집된 raw 데이터
    pass

class GeminiAPIError(AnalysisError):
    """Gemini API 호출 실패."""
    pass

class ResponseParseError(AnalysisError):
    """Gemini 응답 파싱/검증 실패."""
    pass
```

### 10.2 Graceful Degradation 전략

People Scout는 수집 단계별로 다른 에러 처리 전략을 적용한다.

| 수집 단계 | 실패 시 동작 | 심각도 |
|-----------|-------------|--------|
| 프로필 수집 | **에러 raise** (분석 불가) | CRITICAL |
| 포스트 수집 | 경고 로그 + 프로필만으로 분석 계속 | WARNING |
| 팔로우 수집 | 경고 로그 + `network_insights = None` | WARNING |
| LLM 분석 | `AnalysisError` raise (raw_data 포함) | ERROR |
| LLM 응답 파싱 | 1회 재시도, 실패 시 `ResponseParseError` | ERROR |

### 10.3 재시도 전략

```python
# Rate Limit (429) 재시도
MAX_RETRIES = 3
INITIAL_BACKOFF = 2.0  # 초
BACKOFF_MULTIPLIER = 2.0
# 대기 시간: 2초 → 4초 → 8초

# 서버 에러 (5xx) 재시도
MAX_SERVER_ERROR_RETRIES = 3
SERVER_ERROR_BACKOFF = 1.0  # 초

# 타임아웃 재시도
MAX_TIMEOUT_RETRIES = 2
TIMEOUT_SECONDS = 120  # 개별 요청 타임아웃
```

### 10.4 CLI 에러 표시

```
$ people-scout @nonexistent_handle

 Error: 프로필을 찾을 수 없습니다: @nonexistent_handle
 트위터 핸들이 정확한지 확인해주세요.

$ people-scout @kimceo

 Warning: 포스트 수집에 실패했습니다. 프로필 정보만으로 분석합니다.
 (리포트 출력...)
```

---

## 11. 프로젝트 구조

```
people-scout/
├── pyproject.toml                      # 빌드 설정, 의존성, 스크립트
├── PRD.md                              # 이 문서
├── README.md                           # 사용자 가이드, 설치 방법
├── .env.example                        # 환경변수 예시
├── .gitignore                          # Git 무시 파일
├── LICENSE                             # MIT 라이선스
├── src/
│   └── people_scout/
│       ├── __init__.py                 # PeopleScout, PersonReport export
│       ├── scout.py                    # PeopleScout 메인 클래스
│       │                               #   - analyze() / analyze_async()
│       │                               #   - 파이프라인 오케스트레이션
│       ├── cli.py                      # Click CLI 진입점
│       │                               #   - main() 커맨드
│       │                               #   - 옵션 파싱, 출력 라우팅
│       ├── config.py                   # pydantic-settings 기반 설정
│       │                               #   - ScoutSettings 클래스
│       │                               #   - 환경변수 검증
│       ├── errors.py                   # 기본 에러 (PeopleScoutError, ConfigError)
│       ├── selanet/
│       │   ├── __init__.py
│       │   ├── client.py              # SelanetClient
│       │   │                           #   - fetch_profile()
│       │   │                           #   - fetch_posts()
│       │   │                           #   - fetch_follow_list()
│       │   ├── rate_limiter.py        # AsyncRateLimiter
│       │   │                           #   - 분당 5회 토큰 버킷
│       │   │                           #   - acquire() / release()
│       │   ├── models.py             # ScrapeRequest, ScrapeResponse
│       │   └── errors.py             # Selanet 전용 에러
│       ├── analysis/
│       │   ├── __init__.py
│       │   ├── analyzer.py           # GeminiAnalyzer
│       │   │                          #   - analyze_person()
│       │   │                          #   - google-genai SDK 래퍼
│       │   │                          #   - structured output 처리
│       │   ├── prompt.py             # PromptBuilder
│       │   │                          #   - build_system_instruction()
│       │   │                          #   - build_user_prompt()
│       │   │                          #   - format_posts()
│       │   │                          #   - format_follow_list()
│       │   └── models.py            # 분석 결과 모델
│       │                              #   - PersonReport
│       │                              #   - InterestItem
│       │                              #   - CommunicationStyle
│       │                              #   - ContentTypeRatio
│       │                              #   - ConversationEntry
│       │                              #   - NetworkInsights
│       │                              #   - NotableConnection
│       │                              #   - NetworkCluster
│       └── output/
│           ├── __init__.py
│           ├── console.py            # ConsoleRenderer (Rich)
│           │                          #   - render_report()
│           │                          #   - 진행률 스피너
│           ├── json_writer.py        # JsonWriter
│           │                          #   - write(report, path)
│           └── markdown.py           # MarkdownWriter
│                                      #   - write(report, path)
└── tests/
    ├── conftest.py                    # 공통 fixture, mock 설정
    ├── test_scout.py                  # PeopleScout 통합 테스트
    ├── test_selanet_client.py         # SelanetClient 단위 테스트
    ├── test_rate_limiter.py           # RateLimiter 단위 테스트
    ├── test_analysis.py               # GeminiAnalyzer 단위 테스트
    ├── test_prompt.py                 # PromptBuilder 단위 테스트
    ├── test_models.py                 # 데이터 모델 검증 테스트
    ├── test_output.py                 # 출력 모듈 테스트
    ├── test_cli.py                    # CLI 통합 테스트
    └── fixtures/
        ├── twitter_profile.json       # 프로필 API 응답 샘플
        ├── twitter_posts.json         # 포스트 API 응답 샘플
        └── twitter_follows.json       # 팔로우 API 응답 샘플
```

---

## 12. 구현 단계

### Phase 1: 프로젝트 초기화 + Selanet 클라이언트

**목표:** Selanet API와의 안정적인 통신 계층 구축

| 순서 | 작업 | 산출물 |
|------|------|--------|
| 1-1 | pyproject.toml 업데이트 (anthropic -> google-genai) | `pyproject.toml` |
| 1-2 | config.py (pydantic-settings, 환경변수 검증) | `src/people_scout/config.py` |
| 1-3 | errors.py (기본 에러 계층) | `src/people_scout/errors.py` |
| 1-4 | selanet/models.py (ScrapeRequest, ScrapeResponse) | `src/people_scout/selanet/models.py` |
| 1-5 | selanet/errors.py (Selanet 전용 에러) | `src/people_scout/selanet/errors.py` |
| 1-6 | selanet/rate_limiter.py (asyncio 토큰 버킷) | `src/people_scout/selanet/rate_limiter.py` |
| 1-7 | selanet/client.py (httpx + rate limiter + 재시도) | `src/people_scout/selanet/client.py` |
| 1-8 | 테스트 (test_selanet_client, test_rate_limiter, fixtures) | `tests/` |

**의존성:** 없음 (첫 단계)
**예상 산출물:** Selanet API 호출 및 응답 파싱 완료

### Phase 2: 데이터 모델 + Gemini 분석

**목표:** LLM 분석 파이프라인 구축

| 순서 | 작업 | 산출물 |
|------|------|--------|
| 2-1 | analysis/models.py (PersonReport 및 모든 서브 모델) | `src/people_scout/analysis/models.py` |
| 2-2 | analysis/prompt.py (프롬프트 빌더) | `src/people_scout/analysis/prompt.py` |
| 2-3 | analysis/analyzer.py (google-genai SDK 래퍼, structured output) | `src/people_scout/analysis/analyzer.py` |
| 2-4 | 테스트 (test_models, test_prompt, test_analysis) | `tests/` |

**의존성:** Phase 1 완료
**예상 산출물:** 수집된 데이터를 Gemini로 분석하여 PersonReport 생성

### Phase 3: 메인 클래스 + 파이프라인

**목표:** 전체 분석 파이프라인 통합

| 순서 | 작업 | 산출물 |
|------|------|--------|
| 3-1 | scout.py (PeopleScout 클래스, analyze/analyze_async) | `src/people_scout/scout.py` |
| 3-2 | __init__.py (PeopleScout, PersonReport export) | `src/people_scout/__init__.py` |
| 3-3 | 통합 테스트 (test_scout) | `tests/test_scout.py` |

**의존성:** Phase 1 + Phase 2 완료
**예상 산출물:** SDK 사용 가능

### Phase 4: 출력 모듈 + CLI

**목표:** 사용자 인터페이스 완성

| 순서 | 작업 | 산출물 |
|------|------|--------|
| 4-1 | output/console.py (Rich 터미널 출력) | `src/people_scout/output/console.py` |
| 4-2 | output/json_writer.py (JSON 파일 출력) | `src/people_scout/output/json_writer.py` |
| 4-3 | output/markdown.py (마크다운 리포트) | `src/people_scout/output/markdown.py` |
| 4-4 | cli.py (Click CLI) | `src/people_scout/cli.py` |
| 4-5 | 테스트 (test_output, test_cli) | `tests/` |

**의존성:** Phase 3 완료
**예상 산출물:** CLI 및 모든 출력 형식 사용 가능

### Phase 5: 마켓 준비

**목표:** Selanet 마켓플레이스 제출 준비

| 순서 | 작업 | 산출물 |
|------|------|--------|
| 5-1 | README.md (사용 가이드, 설치, 예시) | `README.md` |
| 5-2 | .env.example, .gitignore | 프로젝트 루트 |
| 5-3 | LICENSE (MIT) | `LICENSE` |
| 5-4 | End-to-End 수동 테스트 | 테스트 리포트 |

**의존성:** Phase 4 완료
**예상 산출물:** 배포 가능한 패키지

---

## 13. 비기능 요구사항

### 13.1 성능

| 지표 | 목표 | 비고 |
|------|------|------|
| 기본 분석 (deep=False) | 30초 이내 | API 2회 + LLM 1회 |
| Deep 분석 (deep=True) | 60초 이내 | API 3회 + LLM 1회 |
| LLM 응답 시간 | 15초 이내 | Gemini 2.5 Flash 기준 |
| 메모리 사용량 | 100MB 이내 | 100개 포스트 기준 |

### 13.2 안정성

| 항목 | 요구사항 |
|------|----------|
| Rate Limit 준수 | Selanet 분당 5회 제한 절대 초과하지 않음 |
| 재시도 | 429/5xx에 대해 exponential backoff 적용 |
| Graceful Degradation | 부분 실패 시 가용 데이터로 최선의 결과 제공 |
| 타임아웃 | 개별 요청 120초, 전체 분석 300초 |

### 13.3 사용성

| 항목 | 요구사항 |
|------|----------|
| 설치 | `pip install people-scout` 한 줄로 완료 |
| 최소 설정 | 환경변수 3개 (SELANET_API_KEY, SELANET_BASE_URL, GEMINI_API_KEY) |
| SDK 사용 | 3줄 코드로 분석 결과 획득 |
| 진행 상황 | CLI에서 실시간 진행률 표시 |
| 에러 메시지 | 사용자가 이해할 수 있는 명확한 에러 메시지 |

### 13.4 보안

| 항목 | 요구사항 |
|------|----------|
| API 키 관리 | 환경변수로만 전달, 코드에 하드코딩 금지 |
| 로그 보안 | API 키가 로그에 노출되지 않도록 마스킹 |
| 의존성 | 검증된 공식 SDK만 사용 |
| 데이터 저장 | 분석 결과는 로컬에만 저장, 외부 전송 없음 |

### 13.5 호환성

| 항목 | 요구사항 |
|------|----------|
| Python | 3.11, 3.12, 3.13 지원 |
| OS | macOS, Linux, Windows |
| 패키지 매니저 | pip, uv, poetry 호환 |

### 13.6 테스트

| 항목 | 목표 |
|------|------|
| 단위 테스트 커버리지 | 80% 이상 |
| 통합 테스트 | SDK analyze() 전체 플로우 |
| CLI 테스트 | 주요 옵션 조합 |
| Mock 전략 | 외부 API (Selanet, Gemini) 모두 mock |
| Fixture | 실제 API 응답 기반 fixture 파일 |

---

## 14. 우선순위 (RICE 분석)

| 기능 | Reach | Impact | Confidence | Effort | Score | MoSCoW |
|------|-------|--------|------------|--------|-------|--------|
| 프로필+포스트 수집 | 100 | 3 | 90% | 1w | 270 | Must |
| LLM 분석 (Gemini) | 100 | 3 | 85% | 1w | 255 | Must |
| PersonReport 모델 | 100 | 3 | 95% | 0.5w | 570 | Must |
| CLI 기본 기능 | 80 | 2 | 90% | 0.5w | 288 | Must |
| SDK 인터페이스 | 60 | 2 | 90% | 0.5w | 216 | Must |
| Rate Limiter | 100 | 2 | 95% | 0.5w | 380 | Must |
| 에러 핸들링 | 100 | 2 | 90% | 0.5w | 360 | Must |
| Deep 모드 (네트워크) | 40 | 2 | 80% | 1w | 64 | Should |
| Rich 콘솔 출력 | 80 | 1 | 95% | 0.5w | 152 | Should |
| JSON 출력 | 60 | 1.5 | 95% | 0.3w | 285 | Should |
| 마크다운 출력 | 40 | 1 | 95% | 0.3w | 127 | Could |
| 다국어 (ko/en) | 60 | 1 | 90% | 0.3w | 180 | Should |

---

## 15. 파이프라인 흐름도

```
사용자 입력 (@handle, options)
        │
        ▼
┌──────────────────────┐
│   입력 검증           │  handle 정규화 (@제거/추가)
│   설정 로딩           │  환경변수, .env 파일
└──────────┬───────────┘
           │
           ▼
┌──────────────────────┐
│  Selanet 데이터 수집  │
│                      │
│  1. TWITTER_PROFILE  │──→ 실패 시 CRITICAL: raise
│  2. TWITTER_POST     │──→ 실패 시 WARNING: 계속
│  3. TWITTER_FOLLOW   │──→ 실패 시 WARNING: 스킵 (deep만)
│     (deep mode only) │
└──────────┬───────────┘
           │
           ▼
┌──────────────────────┐
│  프롬프트 구성        │  수집 데이터 → 구조화된 프롬프트
│  (PromptBuilder)     │  + System Instruction
└──────────┬───────────┘
           │
           ▼
┌──────────────────────┐
│  Gemini 2.5 Flash    │  Structured Output
│  (GeminiAnalyzer)    │  → PersonReport JSON
│                      │──→ 실패 시: AnalysisError (raw_data 포함)
└──────────┬───────────┘
           │
           ▼
┌──────────────────────┐
│  응답 파싱/검증       │  JSON → PersonReport (Pydantic)
│                      │──→ 파싱 실패 시: 1회 재시도
└──────────┬───────────┘
           │
           ▼
┌──────────────────────┐
│  출력                 │
│  - console (Rich)    │
│  - JSON 파일         │
│  - Markdown 파일     │
└──────────────────────┘
```

---

## 16. 용어 정의

| 용어 | 정의 |
|------|------|
| Handle | 트위터(X) 사용자명 (@ 접두사 포함/미포함) |
| Deep 모드 | 팔로우 리스트까지 수집하여 네트워크 분석을 포함하는 확장 분석 모드 |
| Selanet | AI 에이전트 마켓플레이스 및 웹 스크래핑 API 제공 플랫폼 |
| Structured Output | LLM이 사전 정의된 JSON 스키마에 맞춰 응답을 생성하는 기능 |
| Graceful Degradation | 일부 기능 실패 시 가용한 데이터로 최선의 결과를 제공하는 전략 |
| Rate Limiter | API 호출 빈도를 제한하여 Rate Limit 초과를 방지하는 모듈 |
| PersonReport | 인물 분석 결과를 담는 최상위 Pydantic 모델 |
