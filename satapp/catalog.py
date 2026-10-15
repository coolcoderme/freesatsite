"""Exam catalogs, topics, and filter helpers."""

EXAMS = ("SAT", "PSAT", "ACT")
DIFFICULTIES = ("Easy", "Medium", "Hard")
QUESTION_TYPES = ("multiple_choice", "grid_in")

SECTIONS = {
    "SAT": ("Reading and Writing", "Math"),
    "PSAT": ("Reading and Writing", "Math"),
    "ACT": ("English", "Math", "Reading", "Science"),
}

TOPICS = {
    "SAT": {
        "Reading and Writing": (
            "Information and Ideas",
            "Craft and Structure",
            "Expression of Ideas",
            "Standard English Conventions",
        ),
        "Math": (
            "Algebra",
            "Advanced Math",
            "Problem-Solving and Data Analysis",
            "Geometry and Trigonometry",
        ),
    },
    "PSAT": {
        "Reading and Writing": (
            "Information and Ideas",
            "Craft and Structure",
            "Expression of Ideas",
            "Standard English Conventions",
        ),
        "Math": (
            "Algebra",
            "Advanced Math",
            "Problem-Solving and Data Analysis",
            "Geometry and Trigonometry",
        ),
    },
    "ACT": {
        "English": ("Grammar and Usage", "Punctuation", "Rhetoric"),
        "Math": ("Pre-Algebra", "Algebra", "Geometry", "Trigonometry"),
        "Reading": (
            "Literary Narrative",
            "Social Science",
            "Humanities",
            "Natural Science",
        ),
        "Science": (
            "Data Representation",
            "Research Summaries",
            "Conflicting Viewpoints",
        ),
    },
}

DEFAULT_MINUTES = {
    ("SAT", "Reading and Writing"): 32,
    ("SAT", "Math"): 35,
    ("PSAT", "Reading and Writing"): 32,
    ("PSAT", "Math"): 35,
    ("ACT", "English"): 45,
    ("ACT", "Math"): 60,
    ("ACT", "Reading"): 35,
    ("ACT", "Science"): 35,
}


def topics_for(exam: str, section: str | None = None) -> list[str]:
    exam_map = TOPICS.get(exam, {})
    if section:
        return list(exam_map.get(section, ()))
    topics: list[str] = []
    for names in exam_map.values():
        topics.extend(names)
    return topics


def suggested_minutes(exam: str, section: str | None, count: int) -> int:
    if section:
        base = DEFAULT_MINUTES.get((exam, section), 30)
        typical = 27 if "Reading" in section or section == "English" else 22
        return max(5, round(base * (count / typical)))
    return max(8, count * 2)
