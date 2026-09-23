from sqlalchemy import Column, Integer, Float, Text, ForeignKey, JSON
from app.models.base import Base

class AnalysisReport(Base):
    __tablename__ = "analysis_reports"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    resume_id = Column(Integer, ForeignKey("resumes.id"))
    job_id = Column(Integer, ForeignKey("job_descriptions.id"))
    ats_score = Column(Float)
    keyword_score = Column(Float)
    semantic_score = Column(Float)
    ai_feedback = Column(JSON) # Store structured AI feedback
