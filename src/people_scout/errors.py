from __future__ import annotations


class PeopleScoutError(Exception):
    """People Scout 기본 예외."""


class ConfigError(PeopleScoutError):
    """설정 오류 (환경변수 누락 등)."""
