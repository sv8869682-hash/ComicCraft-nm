from pathlib import Path
from datetime import datetime

from fpdf import FPDF

from app.config import EXPORTS_DIR


def _pdf_safe(value):
    """
    FPDF Helvetica supports latin-1 only.
    Unsupported characters are safely replaced.
    """
    text = str(value or "")
    return text.encode("latin-1", "replace").decode("latin-1")


def _clean_text(value):
    """
    Prevent extremely long unbroken text from breaking PDF layout.
    """
    text = _pdf_safe(value)
    text = text.replace("\r", " ").replace("\n", "\n")

    # Add spaces around very long continuous strings
    words = text.split(" ")
    fixed_words = []

    for word in words:
        if len(word) > 60:
            chunks = [
                word[i:i + 50]
                for i in range(0, len(word), 50)
            ]
            fixed_words.append(" ".join(chunks))
        else:
            fixed_words.append(word)

    return " ".join(fixed_words)


def _text(pdf, label, value):
    # Label
    pdf.set_font("Helvetica", "B", 12)

    pdf.multi_cell(
        w=180,
        h=7,
        text=_clean_text(label),
        border=0
    )

    # Content
    pdf.set_font("Helvetica", "", 11)

    content = _clean_text(value)

    if content.strip():
        pdf.multi_cell(
            w=180,
            h=6,
            text=content,
            border=0
        )

    pdf.ln(2)


def save_pdf(layout, title="ComicCraft Comic") -> str:

    filename = (
        f"comic_"
        f"{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
    )

    output = EXPORTS_DIR / filename

    pdf = FPDF(
        orientation="P",
        unit="mm",
        format="A4"
    )

    pdf.set_auto_page_break(
        auto=True,
        margin=15
    )

    for panel in layout:

        pdf.add_page()

        pdf.set_title(
            _pdf_safe(title)
        )

        # Panel heading
        pdf.set_font(
            "Helvetica",
            "B",
            18
        )

        heading = (
            f"Panel {panel['panel_number']}: "
            f"{panel['title']}"
        )

        pdf.multi_cell(
            w=180,
            h=10,
            text=_clean_text(heading),
            border=0
        )

        # Panel image
        image_file = Path(
            panel["image_path"]
        )

        if image_file.exists():

            pdf.image(
                str(image_file),
                x=15,
                y=35,
                w=180
            )

            pdf.set_y(165)

        else:

            pdf.ln(10)

        # Panel information
        _text(
            pdf,
            "Scene",
            panel.get(
                "scene_description",
                ""
            )
        )

        _text(
            pdf,
            "Caption",
            panel.get(
                "caption",
                ""
            )
        )

        _text(
            pdf,
            "Narration",
            panel.get(
                "narration",
                ""
            )
        )

        _text(
            pdf,
            "Dialogue",
            panel.get(
                "dialogue",
                ""
            )
        )

    pdf.output(str(output))

    return f"/static/exports/{filename}"