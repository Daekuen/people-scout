from __future__ import annotations

from pydantic_settings import BaseSettings, SettingsConfigDict


class ScoutSettings(BaseSettings):
    """People Scout 환경변수 설정."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # Required
    selanet_api_key: str
    selanet_base_url: str
    gemini_api_key: str

    # Optional
    scout_gemini_model: str = "gemini-2.5-flash"
    scout_default_lang: str = "ko"
    scout_log_level: str = "info"
