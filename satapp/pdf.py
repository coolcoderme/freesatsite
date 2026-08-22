"""Build printable PDF worksheets."""

from __future__ import annotations

from io import BytesIO

from fpdf import FPDF


class WorksheetPDF(FPDF):
    def __init__(self, title: str, include_key: bool = False):
        super().__init__(format="Letter")
        self.worksheet_title = title
        self.include_key = include_key
        self.set_auto_page_break(auto=True, margin=18)
        self.set_margins(16, 16, 16)

    def header(self) -> None:
        self.set_font("Helvetica", "B", 11)
        self.set_text_color(18, 32, 58)
        self.cell(0, 8, self.worksheet_title, new_x="LMARGIN", new_y="NEXT")
        self.set_font("Helvetica", "", 8)
        self.set_text_color(90, 90, 90)
        self.cell(
            0,
            5,
            "Original practice worksheet. Not an official College Board or ACT test.",
            new_x="LMARGIN",
            new_y="NEXT",
        )
        self.ln(2)
        self.set_draw_color(196, 163, 90)
        self.set_line_width(0.6)
        self.line(16, self.get_y(), self.w - 16, self.get_y())
        self.ln(6)

    def footer(self) -> None:
        self.set_y(-14)
        self.set_font("Helvetica", "", 8)
        self.set_text_color(120, 120, 120)
        self.cell(0, 8, f"Page {self.page_no()}/{{nb}}  ·  FreeSAT", align="C")


def _safe(text: str | None) -> str:
    if not text:
        return ""
    replacements = {
        "—": "-",
        "–": "-",
        "“": '"',
        "”": '"',
        "‘": "'",
        "’": "'",
        "×": "x",
        "θ": "theta",
        "²": "^2",
        "³": "^3",
    }
    cleaned = str(text)
    for src, dst in replacements.items():
        cleaned = cleaned.replace(src, dst)
    return cleaned.encode("latin-1", "replace").decode("latin-1")


def render_worksheet(questions: list[dict], title: str, include_key: bool = False) -> bytes:
    pdf = WorksheetPDF(title=title, include_key=include_key)
    pdf.alias_nb_pages()
    pdf.add_page()
    pdf.set_font("Helvetica", "", 10)

    for index, item in enumerate(questions, start=1):
        meta = (
            f"{item.get('exam')}  ·  {item.get('section')}  ·  "
            f"{item.get('topic')}  ·  {item.get('difficulty')}"
        )
        pdf.set_font("Helvetica", "B", 11)
        pdf.set_text_color(18, 32, 58)
        pdf.multi_cell(0, 6, _safe(f"{index}. {meta}"), new_x="LMARGIN", new_y="NEXT")
        if item.get("stimulus"):
            pdf.set_font("Helvetica", "I", 10)
            pdf.set_text_color(40, 40, 40)
            pdf.multi_cell(0, 5, _safe(item["stimulus"]), new_x="LMARGIN", new_y="NEXT")
            pdf.ln(1)
        pdf.set_font("Helvetica", "", 11)
        pdf.set_text_color(20, 20, 20)
        pdf.multi_cell(0, 5.5, _safe(item.get("question", "")), new_x="LMARGIN", new_y="NEXT")
        pdf.ln(1)
        if item.get("type") == "grid_in":
            pdf.set_font("Helvetica", "", 10)
            pdf.cell(0, 8, "Student-produced response: ____________________", new_x="LMARGIN", new_y="NEXT")
        else:
            choices = item.get("choices") or {}
            pdf.set_font("Helvetica", "", 10)
            for letter in ("A", "B", "C", "D"):
                if letter in choices:
                    pdf.multi_cell(
                        0, 5, _safe(f"    {letter})  {choices[letter]}"),
                        new_x="LMARGIN", new_y="NEXT",
                    )
        pdf.ln(4)

    if include_key:
        pdf.add_page()
        pdf.set_font("Helvetica", "B", 14)
        pdf.cell(0, 10, "Answer key", new_x="LMARGIN", new_y="NEXT")
        pdf.ln(2)
        for index, item in enumerate(questions, start=1):
            pdf.set_font("Helvetica", "B", 11)
            pdf.multi_cell(0, 6, _safe(f"{index}. {item.get('answer')}"), new_x="LMARGIN", new_y="NEXT")
            if item.get("explanation"):
                pdf.set_font("Helvetica", "", 10)
                pdf.multi_cell(0, 5, _safe(item["explanation"]), new_x="LMARGIN", new_y="NEXT")
            pdf.ln(2)

    buffer = BytesIO()
    pdf.output(buffer)
    return buffer.getvalue()
