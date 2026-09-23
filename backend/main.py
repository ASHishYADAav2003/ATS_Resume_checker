from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.db.session import engine
from app.models import Base
from app.api.api import api_router

Base.metadata.create_all(bind=engine)

app = FastAPI(title="ATS Compatibility Analyzer", version="1.0.0")

app.include_router(api_router, prefix="/api")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Welcome to the ATS Compatibility Analyzer API"}
