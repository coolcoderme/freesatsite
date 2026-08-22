"""Compare student answers with the key."""

from __future__ import annotations

import re


def normalize_answer(value: str | None, question_type: str = "multiple_choice") -> str:
    text = str(value or "").strip()
    if question_type == "multiple_choice":
        return text[:1].upper()
    compact = re.sub(r"\s+", "", text.replace(",", ""))
    if re.fullmatch(r"-?\d+\.0+", compact):
        compact = compact.split(".", 1)[0]
    return compact


def is_correct(question: dict, given: str | None) -> bool:
    expected = normalize_answer(question.get("answer"), question.get("type", "multiple_choice"))
    actual = normalize_answer(given, question.get("type", "multiple_choice"))
    if not expected or not actual:
        return False
    if question.get("type") == "grid_in":
        try:
            return abs(float(expected) - float(actual)) < 1e-6
        except ValueError:
            return expected.lower() == actual.lower()
    return expected == actual


def grade(questions: list[dict], answers: dict[str, str]) -> dict:
    results = []
    correct = 0
    for item in questions:
        given = answers.get(item["id"], "")
        ok = is_correct(item, given)
        if ok:
            correct += 1
        results.append(
            {
                "id": item["id"],
                "exam": item["exam"],
                "section": item["section"],
                "topic": item["topic"],
                "difficulty": item["difficulty"],
                "question": item["question"],
                "stimulus": item.get("stimulus"),
                "choices": item.get("choices"),
                "type": item["type"],
                "given": given,
                "answer": item.get("answer"),
                "explanation": item.get("explanation"),
                "correct": ok,
            }
        )
    total = len(questions)
    return {
        "correct": correct,
        "total": total,
        "percent": round(100 * correct / total) if total else 0,
        "results": results,
    }
