"""Resolve an optional OpenAI key used only to generate extra questions."""

from __future__ import annotations

import os

from flask import request

from satapp.catalog import SECTIONS, topics_for
from satapp.generate import generate_questions


def resolve_api_key(payload: dict | None = None) -> str:
    data = payload if isinstance(payload, dict) else {}
    return (
        request.values.get("api_key")
        or data.get("api_key")
        or os.environ.get("OPENAI_API_KEY")
        or ""
    ).strip()


def has_server_key() -> bool:
    return bool(os.environ.get("OPENAI_API_KEY", "").strip())


def generation_defaults(filters: dict) -> tuple[str, str, str, str]:
    exam = (filters.get("exam") or "SAT").upper()
    if exam not in SECTIONS:
        exam = "SAT"
    section = filters.get("section") or SECTIONS[exam][0]
    if section not in SECTIONS[exam]:
        section = SECTIONS[exam][0]
    allowed = topics_for(exam, section)
    topic = filters.get("topic") or (allowed[0] if allowed else "Algebra")
    if allowed and topic not in allowed:
        topic = allowed[0]
    difficulty = filters.get("difficulty") or "Medium"
    return exam, section, topic, difficulty


def top_up_questions(filters: dict, questions: list[dict], api_key: str) -> list[dict]:
    """Use the API key only to create items the local bank does not already have."""
    wanted = int(filters.get("count") or 0)
    if not api_key or filters.get("demo_only") or wanted <= len(questions):
        return questions
    exam, section, topic, difficulty = generation_defaults(filters)
    needed = min(10, wanted - len(questions))
    created = generate_questions(
        api_key=api_key,
        exam=exam,
        section=section,
        topic=topic,
        difficulty=difficulty,
        count=needed,
        model=filters.get("model") or "gpt-4o-mini",
    )
    return questions + created
