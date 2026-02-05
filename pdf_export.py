from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
import os
from datetime import datetime


def generate_pdf(overall_risk: str, total_clauses: int) -> str:
    """
    Generates a professional PDF summary of contract risk.
    Compatible with Streamlit Cloud.
    """

    os.makedirs("exports", exist_ok=True)

    filename = f"exports/contract_risk_summary_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"

    c = canvas.Canvas(filename, pagesize=A4)
    width, height = A4

    y = height - 80

    # Title
    c.setFont("Helvetica-Bold", 18)
    c.drawString(60, y, "Contract Risk Summary")
    y -= 40

    # Content
    c.setFont("Helvetica", 12)
    c.drawString(60, y, f"Overall Risk Level: {overall_risk}")
    y -= 25

    c.drawString(60, y, f"Total Clauses Analyzed: {total_clauses}")
    y -= 40

    # Disclaimer
    c.setFont("Helvetica-Oblique", 10)
    c.drawString(
        60,
        y,
        "This report is for awareness only and does not constitute legal advice."
    )

    c.showPage()
    c.save()

    return filename


