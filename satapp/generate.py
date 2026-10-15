"""Create additional practice questions with an OpenAI API key."""

from __future__ import annotations

import json
import re
from typing import Any

from satapp.bank import save_generated, unique_id, load_generated
from satapp.catalog import SECTIONS, topics_for

ALLOWED_MODELS = {
    "gpt-4o-mini",
    "gpt-4o",
    "gpt-4.1-mini",
    "gpt-4.1",
    "o4-mini",
}


def _client(api_key: str):
    from openai import OpenAI

    return OpenAI(api_key=api_key)


def _schema_hint(exam: str, section: str, topic: str, difficulty: str, count: int) -> str:
    return (
        "Return a JSON object with a key named questions whose value is an array. "
        f"Create exactly {count} original practice items for the {exam} {section} "
        f"section, topic {topic}, difficulty {difficulty}. "
        "Do not copy official College Board, Bluebook, Khan Academy, or ACT items. "
        "Each item must include: exam, section, topic, difficulty, type "
        "(multiple_choice or grid_in), stimulus (string or null), question, "
        "choices (object with A-D for multiple_choice, or null for grid_in), "
        "answer (A-D or a numeric string), and explanation. "
        "Passages must be short (80-140 words). Math items should be solvable "
        "without a graphing calculator. Keep language classroom-appropriate."
    )


def _coerce_item(
    raw: dict[str, Any],
    exam: str,
    section: str,
    topic: str,
    difficulty: str,
    reserved: set[str] | None = None,
) -> dict:
    qtype = raw.get("type") or "multiple_choice"
    if qtype not in {"multiple_choice", "grid_in"}:
        qtype = "multiple_choice"
    choices = raw.get("choices")
    if qtype == "multiple_choice":
        if not isinstance(choices, dict):
            choices = {}
        choices = {k: str(choices.get(k, "")).strip() for k in ("A", "B", "C", "D")}
    else:
        choices = None
    prefix = f"gen-{exam}-{section}-{topic}".lower()
    return {
        "id": unique_id(prefix, reserved),
        "exam": exam,
        "section": section,
        "topic": topic,
        "difficulty": difficulty,
        "type": qtype,
        "is_demo": False,
        "generated": True,
        "source": "generated",
        "stimulus": raw.get("stimulus") or None,
        "question": str(raw.get("question", "")).strip(),
        "choices": choices,
        "answer": str(raw.get("answer", "")).strip(),
        "explanation": str(raw.get("explanation", "")).strip(),
    }


def _extract_questions(payload: Any) -> list[dict]:
    if isinstance(payload, dict):
        if isinstance(payload.get("questions"), list):
            return [q for q in payload["questions"] if isinstance(q, dict)]
        if {"question", "answer"} <= set(payload):
            return [payload]
    if isinstance(payload, list):
        return [q for q in payload if isinstance(q, dict)]
    return []


def generate_questions(
    api_key: str,
    exam: str,
    section: str,
    topic: str,
    difficulty: str,
    count: int,
    model: str = "gpt-4o-mini",
) -> list[dict]:
    if not api_key or not api_key.strip():
        raise ValueError("An OpenAI API key is required.")
    exam = exam.upper()
    if exam not in SECTIONS:
        raise ValueError("Choose SAT, PSAT, or ACT.")
    if section not in SECTIONS[exam]:
        raise ValueError(f"{section} is not a {exam} section.")
    allowed_topics = topics_for(exam, section)
    if topic not in allowed_topics and allowed_topics:
        topic = allowed_topics[0]
    count = max(1, min(int(count), 10))
    model = model if model in ALLOWED_MODELS else "gpt-4o-mini"

    client = _client(api_key.strip())
    response = client.chat.completions.create(
        model=model,
        temperature=0.7,
        response_format={"type": "json_object"},
        messages=[
            {
                "role": "system",
                "content": (
                    "You write original standardized-test practice questions "
                    "for teachers and students. Never reproduce copyrighted exams."
                ),
            },
            {
                "role": "user",
                "content": _schema_hint(exam, section, topic, difficulty, count),
            },
        ],
    )
    content = response.choices[0].message.content or "{}"
    try:
        parsed = json.loads(content)
    except json.JSONDecodeError:
        match = re.search(r"\{.*\}", content, flags=re.S)
        parsed = json.loads(match.group(0)) if match else {}

    created = []
    reserved: set[str] = set()
    for raw in _extract_questions(parsed)[:count]:
        item = _coerce_item(raw, exam, section, topic, difficulty, reserved)
        if item["question"] and item["answer"]:
            reserved.add(item["id"])
            created.append(item)
    if not created:
        raise RuntimeError("The model did not return usable questions. Try again.")

    stored = load_generated()
    stored.extend(created)
    save_generated(stored)
    return created
