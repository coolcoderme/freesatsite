"""HTTP routes for worksheets, exams, and generation."""

from __future__ import annotations

import io
import json
import uuid
from datetime import datetime, timezone

from flask import (
    Blueprint,
    abort,
    flash,
    jsonify,
    redirect,
    render_template,
    request,
    send_file,
    session,
    url_for,
)

from satapp.bank import (
    all_questions,
    demo_questions,
    filter_questions,
    get_question,
    pick_questions,
    public_question,
    stats,
)
from satapp.catalog import SECTIONS, suggested_minutes, topics_for
from satapp.generate import ALLOWED_MODELS, generate_questions
from satapp.pdf import render_worksheet
from satapp.scoring import grade

bp = Blueprint("main", __name__)

EXAMS: dict[str, dict] = {}


def _form_filters() -> dict:
    try:
        count = int(request.values.get("count") or 10)
    except ValueError:
        count = 10
    count = max(1, min(count, 40))
    exam = request.values.get("exam")
    demo_only = request.values.get("demo_only") == "1"
    if not exam:
        exam = "" if demo_only else "SAT"
    return {
        "exam": exam,
        "section": request.values.get("section") or "",
        "topic": request.values.get("topic") or "",
        "difficulty": request.values.get("difficulty") or "",
        "count": count,
        "demo_only": demo_only,
        "include_key": request.values.get("include_key") == "1",
        "shuffle": request.values.get("shuffle", "1") == "1",
    }


def _select_questions(filters: dict) -> list[dict]:
    return pick_questions(
        count=filters["count"],
        exam=filters.get("exam"),
        section=filters.get("section") or None,
        topic=filters.get("topic") or None,
        difficulty=filters.get("difficulty") or None,
        demo_only=filters.get("demo_only", False),
        shuffle=filters.get("shuffle", True),
    )


def _worksheet_title(filters: dict) -> str:
    parts = [filters.get("exam") or "Mixed", "practice worksheet"]
    if filters.get("section"):
        parts.insert(1, filters["section"])
    return " ".join(parts)


def _plain_worksheet(questions: list[dict], include_key: bool) -> str:
    lines = ["FreeSAT practice worksheet", "Not an official College Board or ACT test.", ""]
    for index, item in enumerate(questions, start=1):
        lines.append(
            f"{index}. [{item['exam']} · {item['section']} · {item['topic']} · {item['difficulty']}]"
        )
        if item.get("stimulus"):
            lines.append(item["stimulus"])
            lines.append("")
        lines.append(item["question"])
        if item.get("type") == "grid_in":
            lines.append("Student-produced response: ________")
        else:
            for letter, text in (item.get("choices") or {}).items():
                lines.append(f"    {letter}) {text}")
        lines.append("")
    if include_key:
        lines.append("ANSWER KEY")
        lines.append("----------")
        for index, item in enumerate(questions, start=1):
            lines.append(f"{index}. {item.get('answer')}")
            if item.get("explanation"):
                lines.append(f"    {item['explanation']}")
            lines.append("")
    return "\n".join(lines)


@bp.get("/")
def home():
    return render_template(
        "index.html",
        demos=demo_questions(),
        stats=stats(),
    )


@bp.get("/practice")
def practice():
    filters = _form_filters()
    available = filter_questions(
        exam=filters["exam"],
        section=filters["section"] or None,
        topic=filters["topic"] or None,
        difficulty=filters["difficulty"] or None,
        demo_only=filters["demo_only"],
    )
    return render_template(
        "practice.html",
        filters=filters,
        available=len(available),
        minutes=suggested_minutes(filters["exam"], filters["section"] or None, filters["count"]),
    )


@bp.get("/about")
def about():
    return render_template("about.html", stats=stats())


@bp.get("/generate")
def generate_page():
    return render_template(
        "generate.html",
        models=sorted(ALLOWED_MODELS),
        stats=stats(),
    )


@bp.post("/worksheet")
@bp.get("/worksheet")
def worksheet():
    filters = _form_filters()
    questions = _select_questions(filters)
    if not questions:
        flash("No questions match those filters. Try a broader topic or generate more with an API key.")
        return redirect(url_for("main.practice"))
    return render_template(
        "worksheet.html",
        questions=questions,
        filters=filters,
        title=_worksheet_title(filters),
        include_key=filters["include_key"],
        plain=_plain_worksheet(questions, filters["include_key"]),
    )


@bp.post("/download")
def download():
    filters = _form_filters()
    questions = _select_questions(filters)
    if not questions:
        abort(404)
    ids = request.values.getlist("question_id")
    if ids:
        questions = [get_question(qid) for qid in ids]
        questions = [item for item in questions if item]
    fmt = (request.values.get("format") or "pdf").lower()
    title = _worksheet_title(filters)
    stamp = datetime.now(timezone.utc).strftime("%Y%m%d")
    slug = title.lower().replace(" ", "-")

    if fmt == "txt":
        payload = _plain_worksheet(questions, filters["include_key"]).encode("utf-8")
        return send_file(
            io.BytesIO(payload),
            as_attachment=True,
            download_name=f"{slug}-{stamp}.txt",
            mimetype="text/plain",
        )
    if fmt == "json":
        payload = json.dumps(
            [public_question(q, reveal=filters["include_key"]) for q in questions],
            indent=2,
        ).encode("utf-8")
        return send_file(
            io.BytesIO(payload),
            as_attachment=True,
            download_name=f"{slug}-{stamp}.json",
            mimetype="application/json",
        )
    pdf_bytes = render_worksheet(questions, title=title, include_key=filters["include_key"])
    return send_file(
        io.BytesIO(pdf_bytes),
        as_attachment=True,
        download_name=f"{slug}-{stamp}.pdf",
        mimetype="application/pdf",
    )


@bp.post("/exam/start")
def start_exam():
    filters = _form_filters()
    questions = _select_questions(filters)
    if not questions:
        flash("No questions match those filters. Widen the topic or generate more items.")
        return redirect(url_for("main.practice"))
    try:
        minutes = int(request.values.get("minutes") or suggested_minutes(
            filters["exam"], filters["section"] or None, len(questions)
        ))
    except ValueError:
        minutes = suggested_minutes(filters["exam"], filters["section"] or None, len(questions))
    minutes = max(1, min(minutes, 180))
    exam_id = uuid.uuid4().hex
    EXAMS[exam_id] = {
        "id": exam_id,
        "filters": filters,
        "question_ids": [q["id"] for q in questions],
        "minutes": minutes,
        "started": datetime.now(timezone.utc).isoformat(),
        "answers": {},
        "flags": [],
        "submitted": False,
    }
    session["exam_id"] = exam_id
    return redirect(url_for("main.exam_room", exam_id=exam_id))


@bp.get("/exam/<exam_id>")
def exam_room(exam_id: str):
    exam = EXAMS.get(exam_id)
    if not exam:
        abort(404)
    if exam.get("submitted"):
        return redirect(url_for("main.exam_results", exam_id=exam_id))
    questions = [get_question(qid) for qid in exam["question_ids"]]
    questions = [q for q in questions if q]
    return render_template(
        "exam.html",
        exam=exam,
        questions=[public_question(q) for q in questions],
        minutes=exam["minutes"],
    )


@bp.post("/api/exam/<exam_id>/save")
def save_exam(exam_id: str):
    exam = EXAMS.get(exam_id)
    if not exam or exam.get("submitted"):
        abort(404)
    payload = request.get_json(silent=True) or {}
    answers = payload.get("answers") or {}
    flags = payload.get("flags") or []
    if isinstance(answers, dict):
        exam["answers"] = {str(k): str(v) for k, v in answers.items()}
    if isinstance(flags, list):
        exam["flags"] = [str(x) for x in flags]
    return jsonify({"ok": True})


@bp.post("/exam/<exam_id>/submit")
def submit_exam(exam_id: str):
    exam = EXAMS.get(exam_id)
    if not exam:
        abort(404)
    incoming = request.get_json(silent=True) or request.form
    if incoming:
        answers = incoming.get("answers") if isinstance(incoming, dict) else None
        if isinstance(answers, str):
            try:
                answers = json.loads(answers)
            except json.JSONDecodeError:
                answers = {}
        if isinstance(answers, dict):
            exam["answers"].update({str(k): str(v) for k, v in answers.items()})
    questions = [get_question(qid) for qid in exam["question_ids"]]
    questions = [q for q in questions if q]
    report = grade(questions, exam.get("answers") or {})
    exam["submitted"] = True
    exam["report"] = report
    return redirect(url_for("main.exam_results", exam_id=exam_id))


@bp.get("/exam/<exam_id>/results")
def exam_results(exam_id: str):
    exam = EXAMS.get(exam_id)
    if not exam or not exam.get("submitted"):
        abort(404)
    return render_template("results.html", exam=exam, report=exam["report"])


@bp.get("/api/catalog")
def catalog_api():
    exam = request.args.get("exam") or "SAT"
    section = request.args.get("section") or ""
    return jsonify(
        {
            "sections": list(SECTIONS.get(exam, ())),
            "topics": topics_for(exam, section or None),
            "available": len(
                filter_questions(
                    exam=exam,
                    section=section or None,
                    topic=request.args.get("topic") or None,
                    difficulty=request.args.get("difficulty") or None,
                    demo_only=request.args.get("demo_only") == "1",
                )
            ),
        }
    )


@bp.get("/api/questions")
def questions_api():
    filters = _form_filters()
    questions = _select_questions(filters)
    reveal = request.args.get("reveal") == "1"
    return jsonify(
        {
            "count": len(questions),
            "questions": [public_question(q, reveal=reveal) for q in questions],
            "stats": stats(),
        }
    )


@bp.post("/api/generate")
def generate_api():
    payload = request.get_json(silent=True) or request.form
    api_key = (payload.get("api_key") or "").strip()
    if not api_key:
        return jsonify({"ok": False, "error": "Paste an OpenAI API key to create more questions."}), 400
    try:
        created = generate_questions(
            api_key=api_key,
            exam=payload.get("exam") or "SAT",
            section=payload.get("section") or "Reading and Writing",
            topic=payload.get("topic") or "Information and Ideas",
            difficulty=payload.get("difficulty") or "Medium",
            count=int(payload.get("count") or 3),
            model=payload.get("model") or "gpt-4o-mini",
        )
    except Exception as exc:  # noqa: BLE001
        return jsonify({"ok": False, "error": str(exc)}), 400
    return jsonify(
        {
            "ok": True,
            "created": [public_question(q, reveal=True) for q in created],
            "stats": stats(),
        }
    )


@bp.get("/health")
def health():
    return jsonify({"ok": True, "questions": len(all_questions())})
