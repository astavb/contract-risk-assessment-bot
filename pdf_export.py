from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from datetime import datetime
import os


def generate_pdf(
    output_path: str,
    contract_type: str,
    overall_risk: str,
    total_clauses: int,
    clause_summary: list
) -> str:
    """
    Generates a professional PDF risk summary
    """

    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    c = canvas.Canvas(output_path, pagesize=A4)
    width, height = A4

    y = height - 1 * inch

    # Title
    c.setFont("Helvetica-Bold", 18)
    c.drawString(1 * inch, y, "Contract Risk Summary")
    y -= 30

    # Meta info
    c.setFont("Helvetica", 11)
    c.drawString(1 * inch, y, f"Contract Type: {contract_type}")
    y -= 18
    c.drawString(1 * inch, y, f"Overall Risk Level: {overall_risk}")
    y -= 18
    c.drawString(1 * inch, y, f"Total Clauses Analyzed: {total_clauses}")
    y -= 18
    c.drawString(1 * inch, y, f"Generated on: {datetime.now().strftime('%d %b %Y, %H:%M')}")
    y -= 30

    # Clause summary
    c.setFont("Helvetica-Bold", 14)
    c.drawString(1 * inch, y, "Clause Risk Breakdown")
    y -= 20

    c.setFont("Helvetica", 10)

    for idx, clause in enumerate(clause_summary, start=1):
        if y < 1 * inch:
            c.showPage()
            y = height - 1 * inch
            c.setFont("Helvetica", 10)

        text = f"Clause {idx}: {clause['risk']} Risk"
        c.drawString(1 * inch, y, text)
        y -= 14

    # Footer
    y -= 20
    c.setFont("Helvetica-Oblique", 9)
    c.drawString(
        1 * inch,
        y,
        "Disclaimer: This report is for informational purposes only and does not constitute legal advice."
    )

    c.save()
    return output_path
