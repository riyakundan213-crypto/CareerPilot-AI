from fpdf import FPDF
import io

def create_pdf_report(name, top_job, breakdown, skills):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    
    pdf.cell(0, 10, "CareerPilot AI - Resume Report", ln=True, align='C')
    pdf.ln(6)

    pdf.set_font("Arial", size=12)
    pdf.cell(0, 8, f"Name: {name}", ln=True)
    pdf.cell(0, 8, f"Top Job Match: {top_job['Job Role']}", ln=True)
    pdf.cell(0, 8, f"Match Score: {top_job['Match Score (%)']}%", ln=True)
    pdf.ln(4)

    pdf.set_font("Arial", 'B', 12)
    pdf.cell(0, 8, "Skills Matched:", ln=True)
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 6, ", ".join(top_job['Skills Matched']))
    pdf.ln(2)

    pdf.set_font("Arial", 'B', 12)
    pdf.cell(0, 8, "Skills Missing:", ln=True)
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 6, ", ".join(top_job['Skills Missing']))
    pdf.ln(4)

    pdf.set_font("Arial", 'B', 12)
    pdf.cell(0, 8, "ATS Score:", ln=True)
    pdf.set_font("Arial", size=12)
    pdf.cell(0, 8, f"{breakdown['total']} / 100", ln=True)
    pdf.ln(4)

    pdf.set_font("Arial", 'B', 12)
    pdf.cell(0, 8, "Skill Analysis:", ln=True)
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 6, "This report shows matched and missing skills based on your resume.")
    
    buffer = io.BytesIO()
    pdf.output(buffer)
    buffer.seek(0)
    return buffer
