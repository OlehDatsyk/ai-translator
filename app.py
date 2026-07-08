"""
app.py
------
Flask application entrypoint.

Responsibilities of this module ONLY:
    - Wire up HTTP routes.
    - Validate incoming request data.
    - Delegate actual translation work to translator.Translator.
    - Serialize responses as JSON.

Business logic (prompt construction, OpenAI API calls, JSON schema
validation) intentionally lives in translator.py, following the
Single Responsibility Principle and keeping this file thin and testable.
"""

from __future__ import annotations

import logging

from flask import Flask, jsonify, render_template, request
from flask.wrappers import Response

from config import settings
from translator import Translator, TranslationError

# --------------------------------------------------------------------------
# Logging configuration (applies to the whole app, including translator.py
# via the root logger hierarchy).
# --------------------------------------------------------------------------
logging.basicConfig(
    level=getattr(logging, settings.log_level, logging.INFO),
    format="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
)
logger = logging.getLogger(__name__)

# Supported languages shown in the dropdowns. Kept server-side too so the
# backend can validate incoming language names defensively.
SUPPORTED_LANGUAGES: list[str] = [
    "Auto Detect",
    "English",
    "Spanish",
    "French",
    "German",
    "Italian",
    "Portuguese",
    "Dutch",
    "Russian",
    "Ukrainian",
    "Polish",
    "Turkish",
    "Arabic",
    "Hebrew",
    "Hindi",
    "Bengali",
    "Urdu",
    "Chinese (Simplified)",
    "Chinese (Traditional)",
    "Japanese",
    "Korean",
    "Vietnamese",
    "Thai",
    "Indonesian",
    "Malay",
    "Swedish",
    "Norwegian",
    "Danish",
    "Finnish",
    "Greek",
    "Czech",
    "Romanian",
    "Hungarian",
    "Swahili",
]


def create_app() -> Flask:
    """
    Application factory. Using a factory (rather than a bare module-level
    `app = Flask(__name__)`) makes the app easier to test and configure
    for different environments.
    """
    app = Flask(__name__)
    app.config["SECRET_KEY"] = settings.secret_key
    app.config["JSON_SORT_KEYS"] = False

    # Validate configuration early and fail fast with a clear message
    # rather than raising a confusing error on the first API call.
    try:
        settings.validate()
    except RuntimeError as exc:
        logger.error("Configuration error: %s", exc)
        raise

    translator = Translator(
        api_key=settings.openai_api_key,
        model=settings.openai_model,
        default_temperature=settings.default_temperature,
        timeout_seconds=settings.request_timeout_seconds,
    )

    # ----------------------------------------------------------------
    # Routes
    # ----------------------------------------------------------------
    @app.get("/")
    def index() -> str:
        """Render the main translator UI."""
        return render_template("index.html", languages=SUPPORTED_LANGUAGES)

    @app.get("/api/languages")
    def get_languages() -> Response:
        """Return the list of supported languages as JSON."""
        return jsonify({"languages": SUPPORTED_LANGUAGES})

    @app.post("/api/translate")
    def translate() -> tuple[Response, int] | Response:
        """
        Translate text.

        Expected JSON body:
            {
                "text": str,                # required
                "target_language": str,     # required
                "source_language": str,     # optional, defaults to "Auto Detect"
                "temperature": float         # optional, 0.0 - 2.0
            }

        Returns:
            200 with a TranslationResult JSON body on success.
            400 on invalid input.
            502 on upstream (OpenAI) failure.
        """
        payload = request.get_json(silent=True)
        if payload is None:
            return jsonify({"error": "Request body must be valid JSON."}), 400

        text = payload.get("text", "")
        target_language = payload.get("target_language", "")
        source_language = payload.get("source_language") or "Auto Detect"
        temperature = payload.get("temperature")

        if not isinstance(text, str) or not text.strip():
            return jsonify({"error": "Field 'text' is required and cannot be empty."}), 400

        if not isinstance(target_language, str) or not target_language.strip():
            return jsonify({"error": "Field 'target_language' is required."}), 400

        if len(text) > 5000:
            return jsonify(
                {"error": "Text is too long. Please limit input to 5000 characters."}
            ), 400

        parsed_temperature: float | None = None
        if temperature is not None:
            try:
                parsed_temperature = float(temperature)
            except (TypeError, ValueError):
                return jsonify({"error": "Field 'temperature' must be a number."}), 400
            if not (0.0 <= parsed_temperature <= 2.0):
                return jsonify(
                    {"error": "Field 'temperature' must be between 0.0 and 2.0."}
                ), 400

        try:
            result = translator.translate(
                text=text,
                target_language=target_language,
                source_language=source_language,
                temperature=parsed_temperature,
            )
        except TranslationError as exc:
            logger.warning("Translation failed: %s", exc)
            return jsonify({"error": str(exc)}), 502

        return jsonify(result.to_dict())

    # ----------------------------------------------------------------
    # Error handlers
    # ----------------------------------------------------------------
    @app.errorhandler(404)
    def not_found(_error: object) -> tuple[Response, int]:
        return jsonify({"error": "Resource not found."}), 404

    @app.errorhandler(405)
    def method_not_allowed(_error: object) -> tuple[Response, int]:
        return jsonify({"error": "Method not allowed."}), 405

    @app.errorhandler(500)
    def internal_error(error: object) -> tuple[Response, int]:
        logger.exception("Unhandled server error: %s", error)
        return jsonify({"error": "Internal server error."}), 500

    return app


app = create_app()

if __name__ == "__main__":
    app.run(
        host=settings.flask_host,
        port=settings.flask_port,
        debug=settings.flask_debug,
    )
