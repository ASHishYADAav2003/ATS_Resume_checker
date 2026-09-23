from fastapi import APIRouter, Depends, UploadFile, File, HTTPException, status
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.user import User
from app.models.resume import Resume
from app.models.job import JobDescription
from app.api.deps import get_current_user
from app.services.document_parser import parse_document

router = APIRouter()

@router.post("/resume")
async def upload_resume(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if not file.filename.lower().endswith(('.pdf', '.docx')):
        raise HTTPException(status_code=400, detail="Only PDF and DOCX files are supported.")
    
    try:
        contents = await file.read()
        parsed_text = parse_document(file.filename, contents)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
    # Save to db
    resume = Resume(
        user_id=current_user.id,
        file_url=file.filename, # In a real app, this would be an S3 URL
        parsed_text=parsed_text
    )
    db.add(resume)
    db.commit()
    db.refresh(resume)
    
    return {"message": "Resume uploaded and parsed successfully", "resume_id": resume.id}

@router.post("/job-description")
async def upload_job_description(
    title: str,
    company: str,
    file: UploadFile = File(None),
    text_content: str = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    parsed_text = ""
    if file:
        if not file.filename.lower().endswith(('.pdf', '.docx')):
            raise HTTPException(status_code=400, detail="Only PDF and DOCX files are supported.")
        try:
            contents = await file.read()
            parsed_text = parse_document(file.filename, contents)
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))
    elif text_content:
        parsed_text = text_content
    else:
        raise HTTPException(status_code=400, detail="Either file or text_content must be provided.")
        
    job = JobDescription(
        title=title,
        company=company,
        description=parsed_text
    )
    db.add(job)
    db.commit()
    db.refresh(job)
    
    return {"message": "Job description saved successfully", "job_id": job.id}
