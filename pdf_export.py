from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib import colors
from datetime import datetime
import os


def generate_pdf(
    overall_risk,
    total_clauses,
    contract_type="General Contract",
    language="English",
    risk_summary=None
):
    if risk_summary is None:
        risk_summary = {
            "Penalty Clauses": True,
            "Indemnity Clauses": True,
            "Termination Risks": True,
            "IP Ownership Risks": True,
            "Arbitration / Jurisdiction": True
        }

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

    title_style = ParagraphStyle(
        "TitleStyle",
        fontSize=22,
        textColor=colors.white,
        alignment=1,
        spaceAfter=20
    )

    header_bg = Table(
        [[Paragraph("Contract Risk Assessment Summary", title_style)]],
        colWidths=[480]
    )
    header_bg.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#0f172a")),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("PADDING", (0, 0), (-1, -1), 18)
    ]))

    elements.append(header_bg)
    elements.append(Spacer(1, 20))

    meta_style = ParagraphStyle(
        "Meta",
        fontSize=10,
        textColor=colors.grey
    )

    elements.append(Paragraph(
        f"Generated on: {datetime.now().strftime('%d %b %Y, %H:%M')}",
        meta_style
    ))

    elements.append(Spacer(1, 20))

    section_style = ParagraphStyle(
        "Section",
        fontSize=14,
        textColor=colors.HexColor("#0f172a"),
        spaceAfter=10,
        spaceBefore=20,
        fontName="Helvetica-Bold"
    )

    body_style = ParagraphStyle(
        "Body",
        fontSize=11,
        leading=16
    )

    elements.append(Paragraph("Contract Information", section_style))
    elements.append(Paragraph(
        f"""
        <b>Contract Type:</b> {contract_type}<br/>
        <b>Detected Language:</b> {language}<br/>
        <b>Total Clauses Analyzed:</b> {total_clauses}
        """,
        body_style
    ))

    elements.append(Spacer(1, 16))

    risk_color = (
        colors.red if overall_risk == "High Risk"
        else colors.orange if overall_risk == "Medium Risk"
        else colors.green
    )

    risk_box = Table(
        [[Paragraph(f"Overall Contract Risk Level: {overall_risk}", ParagraphStyle(
            "Risk",
            fontSize=14,
            textColor=colors.white,
            alignment=1,
            fontName="Helvetica-Bold"
        ))]],
        colWidths=[480]
    )

    risk_box.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), risk_color),
        ("PADDING", (0, 0), (-1, -1), 14)
    ]))

    elements.append(risk_box)

    elements.append(Spacer(1, 20))

    elements.append(Paragraph("Executive Summary", section_style))
    elements.append(Paragraph(
        """
        This contract was automatically analyzed using an AI-assisted legal risk assessment engine
        designed for small and medium businesses. The analysis identifies potential legal, financial,
        and operational risks based on common contractual patterns.
        <br/><br/>
        The assessment highlights clauses related to penalties, termination rights, indemnities,
        intellectual property ownership, and dispute resolution mechanisms. Business owners are
        strongly advised to review high-risk clauses carefully and seek professional legal advice
        before signing.
        """,
        body_style
    ))

    elements.append(PageBreak())

    elements.append(Paragraph("Key Risk Areas Detected", section_style))

    risk_table_data = [["Risk Area", "Detected"]]
    for k, v in risk_summary.items():
        risk_table_data.append([k, "Yes" if v else "No"])

    risk_table = Table(risk_table_data, colWidths=[300, 180])
    risk_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#e5e7eb")),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ("FONT", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("ALIGN", (1, 1), (-1, -1), "CENTER")
    ]))

    elements.append(risk_table)

    elements.append(PageBreak())

    elements.append(Paragraph("Business Recommendations", section_style))
    elements.append(Paragraph(
        """
        <b>Recommended Actions:</b><br/><br/>
        • Review all high-risk clauses carefully before signing.<br/>
        • Renegotiate one-sided termination, penalty, or indemnity clauses.<br/>
        • Clarify intellectual property ownership and usage rights.<br/>
        • Ensure dispute resolution and jurisdiction terms are acceptable.<br/><br/>
        <b>Signing Guidance:</b><br/>
        This report is intended to assist decision-making but should not replace professional
        legal consultation for critical contracts.
        """,
        body_style
    ))

    elements.append(Spacer(1, 30))

    elements.append(Paragraph(
        "<i>Disclaimer: This report is generated for informational purposes only and does not constitute legal advice.</i>",
        ParagraphStyle("Disclaimer", fontSize=9, textColor=colors.grey)
    ))

    doc.build(elements)
    return file_path



