from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from datetime import datetime
import os


def generate_pdf(
    overall_risk: str,
    total_clauses: int,
    contract_type: str = "General Contract",
    language: str = "English",
    risk_breakdown: dict = None,
    detected_clause_types: list = None
) -> str:
    """
    Generates a detailed PDF contract risk summary.
    """

    os.makedirs("exports", exist_ok=True)

    filename = f"exports/contract_risk_summary_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"

    c = canvas.Canvas(filename, pagesize=A4)
    width, height = A4

    y = height - 60

    # ---------------- TITLE ----------------
    c.setFont("Helvetica-Bold", 18)
    c.drawString(60, y, "Contract Risk Assessment Summary")
    y -= 30

    c.setFont("Helvetica", 11)
    c.drawString(60, y, f"Generated on: {datetime.now().strftime('%d %b %Y, %H:%M')}")
    y -= 30

    # ---------------- BASIC INFO ----------------
    c.setFont("Helvetica-Bold", 12)
    c.drawString(60, y, "Contract Information")
    y -= 20

    c.setFont("Helvetica", 11)
    c.drawString(60, y, f"Contract Type: {contract_type}")
    y -= 18
    c.drawString(60, y, f"Detected Language: {language}")
    y -= 18
    c.drawString(60, y, f"Total Clauses Analyzed: {total_clauses}")
    y -= 30

    # ---------------- RISK SUMMARY ----------------
    c.setFont("Helvetica-Bold", 12)
    c.drawString(60, y, "Overall Risk Assessment")
    y -= 20

    c.setFont("Helvetica", 11)
    c.drawString(60, y, f"Overall Contract Risk Level: {overall_risk}")
    y -= 20

    if risk_breakdown:
        c.drawString(
            60,
            y,
            f"High Risk Clauses: {risk_breakdown.get('High', 0)} | "
            f"Medium Risk Clauses: {risk_breakdown.get('Medium', 0)} | "
            f"Low Risk Clauses: {risk_breakdown.get('Low', 0)}"
        )
        y -= 25

    # ---------------- KEY RISK AREAS ----------------
    if detected_clause_types:
        c.setFont("Helvetica-Bold", 12)
        c.drawString(60, y, "Key Risk Areas Identified")
        y -= 20

        c.setFont("Helvetica", 11)
        for ct in sorted(set(detected_clause_types)):
            c.drawString(70, y, f"- {ct}")
            y -= 16

        y -= 10

    # ---------------- EXECUTIVE SUMMARY ----------------
    c.setFont("Helvetica-Bold", 12)
    c.drawString(60, y, "Executive Summary")
    y -= 20

    c.setFont("Helvetica", 11)

    summary_text = (
        "This contract has been automatically analyzed to identify potential legal "
        "and business risks. The assessment highlights clauses related to penalties, "
        "termination rights, indemnities, intellectual property, and other key areas. "
        "Business owners are advised to review high-risk clauses carefully and seek "
        "professional legal advice before finalizing the agreement."
    )

    text_obj = c.beginText(60, y)
    for line in summary_text.split(". "):
        text_obj.textLine(line.strip())
    c.drawText(text_obj)

    y -= 60

    # ---------------- DISCLAIMER ----------------
    c.setFont("Helvetica-Oblique", 9)
    c.drawString(
        60,
        y,
        "Disclaimer: This report is generated for informational purposes only and does not constitute legal advice."
    )

    c.showPage()
    c.save()

    return filename



