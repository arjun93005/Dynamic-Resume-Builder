from fpdf import FPDF

def export_to_pdf(data: dict, output_path: str = "resume_analysis.pdf"):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    pdf.cell(200, 10, txt="Dynamic Resume Analyzer - Section Extraction Report", ln=True, align="C")
    pdf.ln(10)

    for section, value in data.items():
        pdf.set_font("Arial", "B", size=12)
        pdf.cell(0, 10, txt=f"{section.capitalize()}:", ln=True)
        pdf.set_font("Arial", size=11)
        pdf.multi_cell(0, 8, txt=str(value))
        pdf.ln(6)

    pdf.output(output_path)
    return output_path
