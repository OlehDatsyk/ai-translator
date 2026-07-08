"""
translator.py
--------------
Core translation service.

This module is responsible for ALL communication with the OpenAI Responses
API. It demonstrates:

    - System Prompt        -> a fixed "role" instruction that constrains
                               the model's behaviour every single call.
    - Prompt Engineering    -> a carefully constructed user prompt that
                               gives the model explicit rules and context.
    - Structured Output     -> a JSON Schema passed to the Responses API
                               so the model is forced to return a strict,
                               predictable JSON shape (no free-form text).
    - Temperature            -> a tunable creativity/consistency parameter.
    - JSON parsing            -> safe parsing + validation of the model's
                               structured JSON response into a typed
                               Python object.

The class is deliberately decoupled from Flask (Single Responsibility /
Dependency Inversion): app.py depends on this module's public interface,
not the other way around, so the translation logic could be reused in a
CLI tool, a test suite, or a different web framework without changes.
"""

from __future__ import annotations

import json
import logging
from dataclasses import asdict, dataclass
from typing import Any, Final

from openai import APIConnectionError, APIStatusError, OpenAI, RateLimitError

logger = logging.getLogger(__name__)


# --------------------------------------------------------------------------
# Custom exceptions
# --------------------------------------------------------------------------
class TranslationError(Exception):
    """Raised when a translation request cannot be completed."""


class InvalidTranslationResponse(TranslationError):
    """Raised when the model response does not match the expected schema."""


# --------------------------------------------------------------------------
# Data model
# --------------------------------------------------------------------------
@dataclass(frozen=True)
class TranslationResult:
    """A strongly-typed representation of a single translation result."""

    translated_text: str
    detected_source_language: str
    source_language_code: str
    confidence: float
    notes: str

    def to_dict(self) -> dict[str, Any]:
        """Convert the result into a plain dict (for JSON serialization)."""
        return asdict(self)


# --------------------------------------------------------------------------
# JSON Schema used for Structured Outputs.
# The Responses API guarantees (via json_schema + strict=True) that the
# model's output will validate against this schema, which removes the
# need for fragile regex/string parsing of free-form text.
# --------------------------------------------------------------------------
TRANSLATION_JSON_SCHEMA: Final[dict[str, Any]] = {
    "type": "object",
    "properties": {
        "translated_text": {
            "type": "string",
            "description": "The fully translated text in the target language.",
        },
        "detected_source_language": {
            "type": "string",
            "description": (
                "The human-readable name of the detected (or provided) "
                "source language, e.g. 'French', 'Japanese'."
            ),
        },
        "source_language_code": {
            "type": "string",
            "description": (
                "The ISO 639-1 two-letter code of the detected source "
                "language, e.g. 'fr', 'ja'. Use 'und' if undetermined."
            ),
        },
        "confidence": {
            "type": "number",
            "description": (
                "Model's confidence in the language detection and "
                "translation quality, expressed as a float between 0 and 1."
            ),
        },
        "notes": {
            "type": "string",
            "description": (
                "Optional short notes about tone, idioms, or ambiguity "
                "encountered during translation. Empty string if none."
            ),
        },
    },
    "required": [
        "translated_text",
        "detected_source_language",
        "source_language_code",
        "confidence",
        "notes",
    ],
    "additionalProperties": False,
}


# --------------------------------------------------------------------------
# System prompt: defines the model's persistent role & behavioural rules.
# --------------------------------------------------------------------------
SYSTEM_PROMPT: Final[str] = """\
You are "LinguaBridge", a professional, precise machine translation engine \
embedded inside a web application.

Your responsibilities:
1. Translate the user's text faithfully into the requested target language.
2. If the source language is not provided (auto-detect mode), determine it \
   from the text itself.
3. Preserve tone, formatting, line breaks, and punctuation style as closely \
   as the target language naturally allows.
4. Preserve names, numbers, emails, URLs, and code snippets unchanged unless \
   translation is linguistically required.
5. Never add explanations, commentary, disclaimers, or extra text to the \
   translated_text field — it must contain ONLY the translation itself.
6. If the input text is empty, ambiguous, or already in the target language, \
   still return a valid JSON object following the required schema, using the \
   "notes" field to briefly explain what happened.
7. Always respond using the exact JSON schema provided to you. Do not invent \
   additional fields and do not omit required fields.
8. Be culturally and contextually appropriate; avoid literal word-for-word \
   translation when an idiomatic translation communicates the meaning better.
"""


class Translator:
    """
    Wraps the OpenAI Responses API to provide language translation with
    structured, predictable JSON output.
    """

    def __init__(
        self,
        api_key: str,
        model: str = "gpt-4o-mini",
        default_temperature: float = 0.3,
        timeout_seconds: int = 30,
    ) -> None:
        """
        Args:
            api_key: OpenAI API key (loaded from environment, never hardcoded).
            model: The OpenAI model name to use with the Responses API.
            default_temperature: Sampling temperature used when the caller
                does not explicitly supply one. Lower = more deterministic,
                which is generally desirable for translation accuracy.
            timeout_seconds: Per-request timeout passed to the OpenAI client.
        """
        if not api_key:
            raise ValueError("An OpenAI API key is required to initialize Translator.")

        self._client = OpenAI(api_key=api_key, timeout=timeout_seconds)
        self._model = model
        self._default_temperature = default_temperature

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------
    def translate(
        self,
        text: str,
        target_language: str,
        source_language: str | None = None,
        temperature: float | None = None,
    ) -> TranslationResult:
        """
        Translate `text` into `target_language`.

        Args:
            text: The raw text to translate.
            target_language: Human-readable target language name (e.g. "Spanish").
            source_language: Optional human-readable source language name.
                If None or "Auto Detect", the model will detect it.
            temperature: Optional override for sampling temperature
                (0.0 - 2.0). Defaults to the instance's default_temperature.

        Returns:
            TranslationResult: A validated, typed translation result.

        Raises:
            TranslationError: On any network, API, or validation failure.
        """
        cleaned_text = (text or "").strip()
        if not cleaned_text:
            raise TranslationError("Cannot translate empty text.")

        effective_temperature = (
            temperature if temperature is not None else self._default_temperature
        )
        effective_temperature = max(0.0, min(2.0, effective_temperature))

        user_prompt = self._build_user_prompt(
            text=cleaned_text,
            target_language=target_language,
            source_language=source_language,
        )

        logger.info(
            "Requesting translation | model=%s target=%s source=%s temperature=%.2f",
            self._model,
            target_language,
            source_language or "auto-detect",
            effective_temperature,
        )

        raw_json = self._call_responses_api(
            user_prompt=user_prompt, temperature=effective_temperature
        )
        return self._parse_response(raw_json)

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------
    @staticmethod
    def _build_user_prompt(
        text: str, target_language: str, source_language: str | None
    ) -> str:
        """
        Construct the user-role prompt sent alongside the system prompt.

        This is where prompt engineering happens: we explicitly restate
        the task, constraints, and inputs in a structured way so the
        model has maximum unambiguous context.
        """
        source_clause = (
            f'The source language is "{source_language}".'
            if source_language and source_language.lower() != "auto detect"
            else "The source language is NOT provided — detect it automatically "
            "from the text."
        )

        return (
            f"Task: Translate the text below into \"{target_language}\".\n"
            f"{source_clause}\n\n"
            "Rules:\n"
            "- Return ONLY a JSON object matching the provided schema.\n"
            "- translated_text must contain the translation ONLY "
            "(no notes, no quotes, no explanations).\n"
            "- Keep line breaks from the original text where meaningful.\n\n"
            "Text to translate:\n"
            "-----BEGIN TEXT-----\n"
            f"{text}\n"
            "-----END TEXT-----"
        )

    def _call_responses_api(self, user_prompt: str, temperature: float) -> str:
        """
        Call the OpenAI Responses API with structured output enabled.

        Returns:
            str: The raw JSON string produced by the model.

        Raises:
            TranslationError: Wraps any OpenAI SDK exception into a
                domain-specific error the rest of the app can handle.
        """
        try:
            response = self._client.responses.create(
                model=self._model,
                temperature=temperature,
                input=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": user_prompt},
                ],
                text={
                    "format": {
                        "type": "json_schema",
                        "name": "translation_result",
                        "schema": TRANSLATION_JSON_SCHEMA,
                        "strict": True,
                    }
                },
            )
        except RateLimitError as exc:
            logger.error("OpenAI rate limit exceeded: %s", exc)
            raise TranslationError(
                "The translation service is receiving too many requests right "
                "now. Please wait a moment and try again."
            ) from exc
        except APIConnectionError as exc:
            logger.error("OpenAI connection error: %s", exc)
            raise TranslationError(
                "Could not reach the OpenAI API. Check your internet "
                "connection and try again."
            ) from exc
        except APIStatusError as exc:
            logger.error("OpenAI API returned an error status: %s", exc)
            raise TranslationError(
                f"The translation service returned an error (status "
                f"{exc.status_code}). Please try again later."
            ) from exc
        except Exception as exc:  # noqa: BLE001 - convert any unexpected SDK error
            logger.exception("Unexpected error calling OpenAI Responses API")
            raise TranslationError(
                "An unexpected error occurred while contacting the translation "
                "service."
            ) from exc

        output_text = getattr(response, "output_text", None)
        if not output_text:
            logger.error("Empty output_text from Responses API: %r", response)
            raise TranslationError("The translation service returned an empty response.")

        return output_text

    @staticmethod
    def _parse_response(raw_json: str) -> TranslationResult:
        """
        Parse and validate the raw JSON string returned by the model.

        Even though Structured Outputs guarantees schema conformance,
        we still defensively parse and validate here — never trust
        external input blindly, even from your own model call.

        Raises:
            InvalidTranslationResponse: If parsing or validation fails.
        """
        try:
            data: dict[str, Any] = json.loads(raw_json)
        except json.JSONDecodeError as exc:
            logger.error("Failed to parse JSON from model output: %s", raw_json)
            raise InvalidTranslationResponse(
                "The translation service returned malformed JSON."
            ) from exc

        required_fields = (
            "translated_text",
            "detected_source_language",
            "source_language_code",
            "confidence",
            "notes",
        )
        missing = [field for field in required_fields if field not in data]
        if missing:
            raise InvalidTranslationResponse(
                f"Model response is missing required fields: {', '.join(missing)}"
            )

        try:
            confidence = float(data["confidence"])
        except (TypeError, ValueError) as exc:
            raise InvalidTranslationResponse(
                "Model response 'confidence' field is not numeric."
            ) from exc
        confidence = max(0.0, min(1.0, confidence))

        return TranslationResult(
            translated_text=str(data["translated_text"]),
            detected_source_language=str(data["detected_source_language"]),
            source_language_code=str(data["source_language_code"]),
            confidence=confidence,
            notes=str(data["notes"]),
        )
