"""FreeSAT Flask application factory."""

from __future__ import annotations

import os
from datetime import datetime, timezone

from flask import Flask

from satapp.catalog import DEFAULT_MINUTES, DIFFICULTIES, EXAMS, SECTIONS, TOPICS


def create_app() -> Flask:
    app = Flask(
        __name__,
        template_folder="../templates",
        static_folder="../static",
    )
    app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "freesat-dev-secret")
    app.config["MAX_CONTENT_LENGTH"] = 2 * 1024 * 1024

    from satapp.routes import bp

    app.register_blueprint(bp)

    @app.context_processor
    def inject_globals() -> dict:
        return {
            "EXAMS": EXAMS,
            "SECTIONS": SECTIONS,
            "TOPICS": TOPICS,
            "DIFFICULTIES": DIFFICULTIES,
            "DEFAULT_MINUTES": DEFAULT_MINUTES,
            "current_year": datetime.now(timezone.utc).year,
        }

    return app
