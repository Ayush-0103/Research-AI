from app.services.pdf_generator import PDFGenerator

with open(
    "report.md",
    "r",
    encoding="utf-8"
) as f:

    report = f.read()

pdf = PDFGenerator()

pdf.generate_pdf(report)

print("PDF generated successfully.")