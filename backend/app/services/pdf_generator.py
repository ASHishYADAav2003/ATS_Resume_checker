import io
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from app.models.report import AnalysisReport

def generate_pdf_report(report: AnalysisReport) -> bytes:
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    styles = getSampleStyleSheet()
    
    title_style = styles['Heading1']
    heading2 = styles['Heading2']
    normal_style = styles['Normal']
    
    elements = []
    
    # Title
    elements.append(Paragraph("ATS Compatibility Analysis Report", title_style))
    elements.append(Spacer(1, 12))
    
    # Scores
    elements.append(Paragraph("Scores", heading2))
    elements.append(Paragraph(f"Overall ATS Score: {report.ats_score}%", normal_style))
    elements.append(Paragraph(f"Keyword Score: {report.keyword_score}%", normal_style))
    elements.append(Paragraph(f"Semantic Similarity: {report.semantic_score}%", normal_style))
    elements.append(Spacer(1, 12))
    
    # Keywords
    elements.append(Paragraph("Keyword Analysis", heading2))
    matched = ", ".join(report.ai_feedback.get("matched_keywords", [])) or "None"
    missing = ", ".join(report.ai_feedback.get("missing_keywords", [])) or "None"
    
    elements.append(Paragraph(f"Matched Keywords: {matched}", normal_style))
    elements.append(Paragraph(f"Missing Keywords: {missing}", normal_style))
    elements.append(Spacer(1, 12))
    
    # AI Feedback
    elements.append(Paragraph("AI Review & Suggestions", heading2))
    
    elements.append(Paragraph("Strengths:", styles['Heading3']))
    for item in report.ai_feedback.get("strengths", []):
        elements.append(Paragraph(f"- {item}", normal_style))
        
    elements.append(Paragraph("Weaknesses:", styles['Heading3']))
    for item in report.ai_feedback.get("weaknesses", []):
        elements.append(Paragraph(f"- {item}", normal_style))
        
    elements.append(Paragraph("Suggestions:", styles['Heading3']))
    for item in report.ai_feedback.get("suggestions", []):
        elements.append(Paragraph(f"- {item}", normal_style))
        
    doc.build(elements)
    
    pdf_bytes = buffer.getvalue()
    buffer.close()
    return pdf_bytes
