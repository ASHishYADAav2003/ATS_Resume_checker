from sqlalchemy import Column, Integer, String, Text, ForeignKey
from app.models.base import Base

class Resume(Base):
    __tablename__ = "resumes"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    file_url = Column(String)
    parsed_text = Column(Text)
