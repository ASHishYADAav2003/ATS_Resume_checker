from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.user import User
from app.models.resume import Resume
from app.models.job import JobDescription
from app.models.report import AnalysisReport
from app.api.deps import get_current_user
from app.services.nlp_engine import extract_keywords, calculate_similarity, detect_risks, generate_ai_feedback

router = APIRouter()

@router.post("/analyze/{resume_id}/{job_id}")
async def analyze_resume(
    resume_id: int,
    job_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    resume = db.query(Resume).filter(Resume.id == resume_id, Resume.user_id == current_user.id).first()
    job = db.query(JobDescription).filter(JobDescription.id == job_id).first()
    
    if not resume or not job:
        raise HTTPException(status_code=404, detail="Resume or Job Description not found.")
        
    resume_text = resume.parsed_text
    job_text = job.description
    
    # 1. Keyword Extraction & Gap Analysis
    resume_keywords = extract_keywords(resume_text)
    job_keywords = extract_keywords(job_text)
    
    matched_keywords = resume_keywords.intersection(job_keywords)
    missing_keywords = job_keywords.difference(resume_keywords)
    extra_keywords = resume_keywords.difference(job_keywords)
    
    keyword_score = 0
    if len(job_keywords) > 0:
        keyword_score = (len(matched_keywords) / len(job_keywords)) * 100
        
    # 2. Semantic Similarity Engine
    semantic_score = calculate_similarity(resume_text, job_text)
    
    # 3. Overall ATS Score (weighted combination)
    ats_score = (keyword_score * 0.4) + (semantic_score * 0.6)
    
    # 4. ATS Risk Detection
    risks = detect_risks(resume_text)
    
    # 5. AI Resume Review (Mock or real OpenAI)
    ai_feedback = await generate_ai_feedback(resume_text, job_text)
    
    report_data = {
        "ats_score": round(ats_score, 2),
        "keyword_score": round(keyword_score, 2),
        "semantic_score": round(semantic_score, 2),
        "matched_keywords": list(matched_keywords),
        "missing_keywords": list(missing_keywords),
        "extra_keywords": list(extra_keywords),
        "risks": risks,
        "ai_feedback": ai_feedback
    }
    
    report = AnalysisReport(
        user_id=current_user.id,
        resume_id=resume.id,
        job_id=job.id,
        ats_score=report_data["ats_score"],
        keyword_score=report_data["keyword_score"],
        semantic_score=report_data["semantic_score"],
        ai_feedback=report_data
    )
    
    db.add(report)
    db.commit()
    db.refresh(report)
    
    return {"message": "Analysis complete", "report_id": report.id, "data": report_data}
    
@router.get("/report/{report_id}")
def get_report(
    report_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    report = db.query(AnalysisReport).filter(AnalysisReport.id == report_id, AnalysisReport.user_id == current_user.id).first()
    if not report:
        raise HTTPException(status_code=404, detail="Report not found")
        
    return {
        "id": report.id,
        "ats_score": report.ats_score,
        "keyword_score": report.keyword_score,
        "semantic_score": report.semantic_score,
        "details": report.ai_feedback
    }

from fastapi.responses import Response
from app.services.pdf_generator import generate_pdf_report

@router.get("/report/{report_id}/download")
def download_report(
    report_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    report = db.query(AnalysisReport).filter(AnalysisReport.id == report_id, AnalysisReport.user_id == current_user.id).first()
    if not report:
        raise HTTPException(status_code=404, detail="Report not found")
        
    pdf_bytes = generate_pdf_report(report)
    
    return Response(
        content=pdf_bytes,
        media_type="application/pdf",
        headers={"Content-Disposition": f"attachment; filename=ATS_Report_{report_id}.pdf"}
    )
