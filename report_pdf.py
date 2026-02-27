"""
Generate a simple PDF report with an 'EY NOX REPORT' heading and
the investigation summary as body text. Logo support is intentionally
disabled to keep dependencies and layout minimal.
"""
from io import BytesIO

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer


def build_report_pdf(summary_markdown: str, logo_path=None) -> bytes:
    """
    Build a PDF report with 'EY NOX REPORT' heading and summary content.
    Returns the PDF as raw bytes.
    """
    buffer = BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=inch,
        leftMargin=inch,
        topMargin=inch,
        bottomMargin=inch,
    )
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        name="ReportTitle",
        parent=styles["Heading1"],
        fontSize=18,
        spaceAfter=12,
    )
    body_style = ParagraphStyle(
        name="ReportBody",
        parent=styles["Normal"],
        fontSize=10,
        leading=14,
    )

    story = []
    # Header without logo
    story.append(Paragraph("EY NOX REPORT", title_style))

    story.append(Spacer(1, 0.25 * inch))

    # Body: summary text (markdown as plain paragraphs)
    for block in summary_markdown.split("\n\n"):
        block = block.strip()
        if not block:
            continue
        # Simple handling: treat lines starting with ### or ## or # as headings
        lines = block.split("\n")
        for line in lines:
            line = line.strip()
            if not line:
                continue
            if line.startswith("### "):
                story.append(Paragraph(line[4:], styles["Heading3"]))
            elif line.startswith("## "):
                story.append(Paragraph(line[3:], styles["Heading2"]))
            elif line.startswith("# "):
                story.append(Paragraph(line[2:], styles["Heading1"]))
            elif line.startswith("|") and "---" not in line:
                # Table row – render as plain text for simplicity
                story.append(Paragraph(line.replace("|", " &bull; "), body_style))
            else:
                # Escape XML for ReportLab
                escaped = line.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
                story.append(Paragraph(escaped, body_style))
        story.append(Spacer(1, 6))

    doc.build(story)
    return buffer.getvalue()
