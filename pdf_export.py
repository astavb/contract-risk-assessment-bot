from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

def generate_pdf(summary, filename="contract_summary.pdf"):
    c = canvas.Canvas(filename, pagesize=A4)
    text = c.beginText(40, 800)

    for line in summary.split("\n"):
        text.textLine(line)

    c.drawText(text)
    c.save()

    return filename
