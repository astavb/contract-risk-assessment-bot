from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib import colors
from datetime import datetime
import os


def generate_pdf(
    overall_risk,
    total_clauses,
    contract_type="General Contract",
    language="English",
):
    os.makedirs("pdf_reports", exist_ok=True)
    file_path = f"pdf_reports/contract_risk_summary_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"

    doc = SimpleDocTemplate(
        file_path,
        pagesize=A4,
        rightMargin=40,
        leftMargin=40,
        topMargin=40,
        bottomMargin=40
    )

    styles = getSampleStyleSheet()
    elements = []

    # ---------- COVER HEADER ----------
    header = Table(
        [[Paragraph(
            "Contract Risk Assessment Report",
            ParagraphStyle(
                "Header",
                fontSize=24,
                textColor=colors.white,
                alignment=1,
                fontName="Helvetica-Bold"
            )
        )]],
        colWidths=[480]
    )

    header.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#0f172a")),
        ("PADDING", (0, 0), (-1, -1), 20)
    ]))

    elements.append(header)
    elements.append(Spacer(1, 18))

    elements.append(Paragraph(
        f"Generated on {datetime.now().strftime('%d %b %Y, %H:%M')}",
        ParagraphStyle("Meta", fontSize=10, textColor=colors.grey)
    ))

    elements.append(Spacer(1, 24))

    # ---------- CONTRACT INFO CARD ----------
    elements.append(Paragraph(
        "Contract Information",
        ParagraphStyle("Section", fontSize=15, fontName="Helvetica-Bold")
    ))

    info_table = Table(
        [
            ["Contract Type", contract_type],
            ["Detected Language", language],
            ["Total Clauses Analyzed", str(total_clauses)]
        ],
        colWidths=[180, 300]
    )

    info_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#f8fafc")),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.lightgrey),
        ("FONT", (0, 0), (0, -1), "Helvetica-Bold"),
        ("PADDING", (0, 0), (-1, -1), 10)
    ]))

    elements.append(Spacer(1, 12))
    elements.append(info_table)
    elements.append(Spacer(1, 26))

    # ---------- RISK BADGE ----------
    risk_color = (
        colors.red if overall_risk == "High Risk"
        else colors.orange if overall_risk == "Medium Risk"
        else colors.green
    )

    risk_box = Table(
        [[Paragraph(
            f"Overall Contract Risk: {overall_risk}",
            ParagraphStyle(
                "Risk",
                fontSize=14,
                textColor=colors.white,
                alignment=1,
                fontName="Helvetica-Bold"
            )
        )]],
        colWidths=[480]
    )

    risk_box.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), risk_color),
        ("PADDING", (0, 0), (-1, -1), 14),
        ("TOPPADDING", (0, 0), (-1, -1), 16),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 16),
    ]))

    elements.append(risk_box)
    elements.append(Spacer(1, 30))

    # ---------- EXECUTIVE SUMMARY ----------
    elements.append(Paragraph(
        "Executive Summary",
        ParagraphStyle("Section", fontSize=15, fontName="Helvetica-Bold")
    ))

    elements.append(Spacer(1, 10))

    elements.append(Paragraph(
        """
        This contract has been automatically reviewed using an AI-assisted legal risk
        assessment engine designed specifically for small and medium businesses.
        <br/><br/>
        The analysis identifies potential legal, financial, and operational risks based on
        common contractual patterns such as penalties, termination rights, indemnities,
        intellectual property ownership, and dispute resolution clauses.
        <br/><br/>
        Business owners are strongly advised to carefully review high-risk clauses and seek
        professional legal advice before signing or renewing the agreement.
        """,
        ParagraphStyle("Body", fontSize=11, leading=16)
    ))

    elements.append(Spacer(1, 40))

    # ---------- DISCLAIMER ----------
    elements.append(Paragraph(
        "<i>Disclaimer: This report is generated for informational purposes only and does not constitute legal advice.</i>",
        ParagraphStyle("Disclaimer", fontSize=9, textColor=colors.grey)
    ))

    doc.build(elements)
    return file_path


