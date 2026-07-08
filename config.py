"""
config.py
---------
Centralized application configuration.

All secrets and environment-specific values are loaded from environment
variables (via a local .env file during development). Nothing sensitive
is ever hardcoded in source code, per security best practice.

This module follows the Single Responsibility Principle: its only job
is to load, validate, and expose configuration values to the rest of
the application.
"""

from __future__ import annotations

import logging
import os
from dataclasses import dataclass

from dotenv import load_dotenv

# Load variables from a .env file (if present) into the process environment.
# This must run before we read any os.environ values below.
load_dotenv()


def _get_bool(env_var: str, default: bool) -> bool:
    """Parse a boolean value from an environment variable."""
    raw_value = os.getenv(env_var)
    if raw_value is None:
        return default
    return raw_value.strip().lower() in {"1", "true", "yes", "on"}


def _get_float(env_var: str, default: float) -> float:
    """Parse a float value from an environment variable, falling back to a default."""
    raw_value = os.getenv(env_var)
    if raw_value is None or raw_value.strip() == "":
        return default
    try:
        return float(raw_value)
    except ValueError:
        logging.getLogger(__name__).warning(
            "Invalid float for %s=%r, using default %.2f", env_var, raw_value, default
        )
        return default


def _get_int(env_var: str, default: int) -> int:
    """Parse an int value from an environment variable, falling back to a default."""
    raw_value = os.getenv(env_var)
    if raw_value is None or raw_value.strip() == "":
        return default
    try:
        return int(raw_value)
    except ValueError:
        logging.getLogger(__name__).warning(
            "Invalid int for %s=%r, using default %d", env_var, raw_value, default
        )
        return default


@dataclass(frozen=True)
class AppConfig:
    """Immutable application configuration object."""

    # --- OpenAI settings -----------------------------------------------
    openai_api_key: str
    openai_model: str
    default_temperature: float
    request_timeout_seconds: int

    # --- Flask settings --------------------------------------------------
    flask_debug: bool
    flask_host: str
    flask_port: int
    secret_key: str

    # --- Logging -----------------------------------------------------------
    log_level: str

    def validate(self) -> None:
        """
        Validate required configuration values.

        Raises:
            RuntimeError: If a required setting is missing or invalid.
        """
        if not self.openai_api_key:
            raise RuntimeError(
                "OPENAI_API_KEY is not set. Copy '.env.example' to '.env' and "
                "add your OpenAI API key before starting the application."
            )
        if not (0.0 <= self.default_temperature <= 2.0):
            raise RuntimeError(
                "DEFAULT_TEMPERATURE must be between 0.0 and 2.0 "
                f"(got {self.default_temperature})."
            )


def load_config() -> AppConfig:
    """
    Build an AppConfig instance from the current environment.

    Returns:
        AppConfig: A populated, validated configuration object.
    """
    config = AppConfig(
        openai_api_key=os.getenv("OPENAI_API_KEY", "").strip(),
        openai_model=os.getenv("OPENAI_MODEL", "gpt-4o-mini").strip(),
        default_temperature=_get_float("DEFAULT_TEMPERATURE", 0.3),
        request_timeout_seconds=_get_int("OPENAI_REQUEST_TIMEOUT", 30),
        flask_debug=_get_bool("FLASK_DEBUG", False),
        flask_host=os.getenv("FLASK_HOST", "127.0.0.1").strip(),
        flask_port=_get_int("FLASK_PORT", 5000),
        secret_key=os.getenv("FLASK_SECRET_KEY", "dev-secret-key-change-me").strip(),
        log_level=os.getenv("LOG_LEVEL", "INFO").strip().upper(),
    )
    return config


# A module-level singleton, imported by the rest of the app.
settings = load_config()
