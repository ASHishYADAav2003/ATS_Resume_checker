from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    PROJECT_NAME: str = "ATS Compatibility Analyzer API"
    DATABASE_URL: str = "postgresql://ats_user:ats_password@localhost:5432/ats_db"
    SECRET_KEY: str = "supersecretjwtkeythatshouldbechangedinproduction"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    OPENAI_API_KEY: Optional[str] = None
    
    class Config:
        env_file = ".env"

settings = Settings()
