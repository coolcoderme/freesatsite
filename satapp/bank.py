"""Load, filter, and persist practice questions."""

from __future__ import annotations

import json
import random
import re
from copy import deepcopy
from pathlib import Path

from satapp.catalog import DIFFICULTIES, EXAMS
from satapp.seed import QUESTIONS

DATA_DIR = Path(__file__).resolve().parent.parent / "data"
GENERATED_PATH = DATA_DIR / "generated.json"

_ID_SAFE = re.compile(r"[^a-zA-Z0-9._-]+")


def _normalize(question: dict) -> dict:
    item = deepcopy(question)
    item.setdefault("stimulus", None)
    item.setdefault("choices", None)
    item.setdefault("is_demo", False)
    item.setdefault("source", "built-in" if not item.get("generated") else "generated")
    item.setdefault("type", "multiple_choice")
    item["exam"] = str(item.get("exam", "")).upper()
    if item["exam"] not in EXAMS:
        item["exam"] = "SAT"
    difficulty = str(item.get("difficulty", "Medium")).title()
    item["difficulty"] = difficulty if difficulty in DIFFICULTIES else "Medium"
    if item["type"] == "multiple_choice" and not item.get("choices"):
        item["choices"] = {"A": "", "B": "", "C": "", "D": ""}
    item["answer"] = str(item.get("answer", "")).strip()
    return item


def load_generated() -> list[dict]:
    if not GENERATED_PATH.exists():
        return []
    try:
        payload = json.loads(GENERATED_PATH.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return []
    if isinstance(payload, dict):
        payload = payload.get("questions", [])
    if not isinstance(payload, list):
        return []
    return [_normalize(q) for q in payload if isinstance(q, dict) and q.get("id")]


def save_generated(questions: list[dict]) -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    GENERATED_PATH.write_text(
        json.dumps(questions, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )


def all_questions() -> list[dict]:
    built_in = [_normalize(q) for q in QUESTIONS]
    generated = load_generated()
    seen = {q["id"] for q in built_in}
    merged = built_in[:]
    for item in generated:
        if item["id"] in seen:
            continue
        merged.append(item)
        seen.add(item["id"])
    return merged


def demo_questions() -> list[dict]:
    return [q for q in all_questions() if q.get("is_demo")]


def get_question(question_id: str) -> dict | None:
    for item in all_questions():
        if item["id"] == question_id:
            return item
    return None


def _match(value: str | None, expected: str | None) -> bool:
    if not expected or expected.lower() in {"any", "all", ""}:
        return True
    return str(value or "").lower() == expected.lower()


def filter_questions(
    exam: str | None = None,
    section: str | None = None,
    topic: str | None = None,
    difficulty: str | None = None,
    demo_only: bool = False,
    include_generated: bool = True,
) -> list[dict]:
    pool = all_questions() if include_generated else [_normalize(q) for q in QUESTIONS]
    selected = []
    for item in pool:
        if demo_only and not item.get("is_demo"):
            continue
        if not _match(item.get("exam"), exam):
            continue
        if not _match(item.get("section"), section):
            continue
        if not _match(item.get("topic"), topic):
            continue
        if not _match(item.get("difficulty"), difficulty):
            continue
        selected.append(item)
    return selected


def pick_questions(
    count: int,
    exam: str | None = None,
    section: str | None = None,
    topic: str | None = None,
    difficulty: str | None = None,
    demo_only: bool = False,
    shuffle: bool = True,
) -> list[dict]:
    pool = filter_questions(
        exam=exam,
        section=section,
        topic=topic,
        difficulty=difficulty,
        demo_only=demo_only,
    )
    if shuffle:
        pool = pool[:]
        random.shuffle(pool)
    count = max(1, min(int(count), 60, len(pool) or 1))
    return pool[: min(count, len(pool))]


def public_question(item: dict, reveal: bool = False) -> dict:
    payload = {
        "id": item["id"],
        "exam": item["exam"],
        "section": item["section"],
        "topic": item["topic"],
        "difficulty": item["difficulty"],
        "type": item["type"],
        "is_demo": bool(item.get("is_demo")),
        "stimulus": item.get("stimulus"),
        "question": item["question"],
        "choices": item.get("choices"),
        "source": item.get("source", "built-in"),
    }
    if reveal:
        payload["answer"] = item.get("answer")
        payload["explanation"] = item.get("explanation")
    return payload


def unique_id(prefix: str, reserved: set[str] | None = None) -> str:
    base = _ID_SAFE.sub("-", prefix).strip("-").lower() or "q"
    existing = {q["id"] for q in all_questions()}
    if reserved:
        existing |= reserved
    n = 1
    while True:
        candidate = f"{base}-{n:03d}"
        if candidate not in existing:
            return candidate
        n += 1


def stats() -> dict:
    items = all_questions()
    by_exam: dict[str, int] = {}
    for item in items:
        by_exam[item["exam"]] = by_exam.get(item["exam"], 0) + 1
    return {
        "total": len(items),
        "demo": sum(1 for q in items if q.get("is_demo")),
        "generated": sum(1 for q in items if q.get("source") == "generated"),
        "by_exam": by_exam,
    }
