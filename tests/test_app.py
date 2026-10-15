import pytest

from satapp import create_app
from satapp.bank import demo_questions, filter_questions, pick_questions
from satapp.scoring import grade, is_correct


@pytest.fixture()
def client():
    app = create_app()
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_demo_bank_has_ten_questions():
    demos = demo_questions()
    assert len(demos) == 10
    exams = {item["exam"] for item in demos}
    assert exams == {"SAT", "PSAT", "ACT"}


def test_filters_respect_exam_and_difficulty():
    sat_math = filter_questions(exam="SAT", section="Math")
    assert sat_math
    assert all(item["exam"] == "SAT" and item["section"] == "Math" for item in sat_math)
    easy = filter_questions(difficulty="Easy")
    assert easy
    assert all(item["difficulty"] == "Easy" for item in easy)


def test_pick_questions_caps_to_pool():
    selected = pick_questions(count=80, demo_only=True, shuffle=False)
    assert len(selected) == 10


def test_grid_in_scoring_accepts_equivalent_numbers():
    question = {"type": "grid_in", "answer": "7"}
    assert is_correct(question, "7")
    assert is_correct(question, "7.0")
    assert not is_correct(question, "8")


def test_grade_counts_blanks_as_incorrect():
    questions = [
        {"id": "a", "exam": "SAT", "section": "Math", "topic": "Algebra", "difficulty": "Easy",
         "type": "multiple_choice", "question": "q", "answer": "B"},
    ]
    report = grade(questions, {})
    assert report["correct"] == 0
    assert report["total"] == 1


def test_home_and_practice_pages(client):
    assert client.get("/").status_code == 200
    assert client.get("/practice").status_code == 200
    assert client.get("/generate").status_code == 200
    assert client.get("/about").status_code == 200
    health = client.get("/health").get_json()
    assert health["ok"] is True
    assert health["questions"] >= 10


def test_worksheet_and_downloads(client):
    page = client.post("/worksheet", data={"exam": "SAT", "count": 4, "include_key": "1"})
    assert page.status_code == 200
    assert b"practice worksheet" in page.data

    pdf = client.post("/download", data={"exam": "PSAT", "count": 3, "format": "pdf"})
    assert pdf.status_code == 200
    assert pdf.data[:4] == b"%PDF"

    text = client.post("/download", data={"demo_only": "1", "count": 10, "format": "txt"})
    assert text.status_code == 200
    assert b"FreeSAT practice worksheet" in text.data


def test_exam_flow_scores_answers(client):
    start = client.post(
        "/exam/start",
        data={"demo_only": "1", "count": 10, "minutes": 12},
        follow_redirects=False,
    )
    assert start.status_code == 302
    exam_id = start.headers["Location"].rstrip("/").split("/")[-1]
    room = client.get(f"/exam/{exam_id}")
    assert room.status_code == 200
    assert b"Deskbook" in room.data

    demos = demo_questions()
    answers = {item["id"]: item["answer"] for item in demos[:8]}
    answers[demos[8]["id"]] = "Z"
    client.post(
        f"/api/exam/{exam_id}/save",
        json={"answers": answers, "flags": [demos[0]["id"]]},
    )
    submit = client.post(
        f"/exam/{exam_id}/submit",
        json={"answers": answers},
        follow_redirects=False,
    )
    assert submit.status_code == 302
    results = client.get(f"/exam/{exam_id}/results")
    assert results.status_code == 200
    assert b"8 / 10 correct" in results.data


def test_catalog_api(client):
    data = client.get("/api/catalog?exam=ACT&section=Science").get_json()
    assert "Data Representation" in data["topics"]
    assert data["available"] >= 1


def test_generate_requires_key(client, monkeypatch):
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    response = client.post("/api/generate", json={"exam": "SAT", "count": 1})
    assert response.status_code == 400
    body = response.get_json()
    assert body["ok"] is False
    assert "additional questions" in body["error"]


def test_practice_works_without_api_key(client, monkeypatch):
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    page = client.get("/practice")
    assert page.status_code == 200
    assert b"optional" in page.data
    assert b"Additional questions" in page.data
    worksheet = client.post("/worksheet", data={"exam": "SAT", "count": 3})
    assert worksheet.status_code == 200
    assert b"practice worksheet" in worksheet.data


def test_builder_generates_only_the_extra_questions(client, monkeypatch):
    calls = []

    def fake_generate(**kwargs):
        calls.append(kwargs)
        return [{
            "id": "gen-extra-001",
            "exam": kwargs["exam"],
            "section": kwargs["section"],
            "topic": kwargs["topic"],
            "difficulty": kwargs["difficulty"],
            "type": "multiple_choice",
            "is_demo": False,
            "source": "generated",
            "stimulus": None,
            "question": "Generated extra item?",
            "choices": {"A": "1", "B": "2", "C": "3", "D": "4"},
            "answer": "A",
            "explanation": "Because it was generated.",
        }]

    monkeypatch.setattr("satapp.keys.generate_questions", fake_generate)
    pool = filter_questions(exam="ACT", section="Science", difficulty="Hard")
    assert pool
    page = client.post(
        "/worksheet",
        data={
            "exam": "ACT",
            "section": "Science",
            "difficulty": "Hard",
            "count": len(pool) + 1,
            "api_key": "sk-test",
        },
    )
    assert page.status_code == 200
    assert calls
    assert calls[0]["api_key"] == "sk-test"
    assert calls[0]["count"] == 1
    assert b"Generated extra item?" in page.data


def test_builder_skips_generation_when_bank_is_enough(client, monkeypatch):
    def fail_generate(**kwargs):
        raise AssertionError("should not generate when the bank already has enough")

    monkeypatch.setattr("satapp.keys.generate_questions", fail_generate)
    page = client.post("/worksheet", data={"exam": "SAT", "count": 2, "api_key": "sk-test"})
    assert page.status_code == 200
    assert b"practice worksheet" in page.data
