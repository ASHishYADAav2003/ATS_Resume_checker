# ATS Compatibility Analyzer

An AI-powered Applicant Tracking System (ATS) compatibility analyzer that evaluates a candidate's resume against a job description.

## Tech Stack
- **Frontend:** React, TypeScript, Vite, Tailwind CSS, Recharts
- **Backend:** Python FastAPI, SQLAlchemy, PostgreSQL
- **AI/NLP:** spaCy, Sentence Transformers, OpenAI API
- **Document Parsing:** PyPDF2, pdfplumber, python-docx, ReportLab

## Getting Started

### Prerequisites
- Node.js (v18+)
- Python (3.11+)
- Docker and Docker Compose (for database)

### Backend Setup
1. Create a `.env` file in the `backend` directory based on the configuration in `app/core/config.py`.
2. Start the database using Docker Compose:
   ```bash
   docker-compose up -d db
   ```
3. Install dependencies:
   ```bash
   cd backend
   pip install -r requirements.txt
   python -m spacy download en_core_web_sm
   ```
4. Run the FastAPI server:
   ```bash
   cd backend
   uvicorn main:app --reload
   ```

### Frontend Setup
1. Install dependencies:
   ```bash
   cd frontend
   npm install
   ```
2. Start the development server:
   ```bash
   npm run dev
   ```

## Features
- **Resume Upload:** Parse PDF and DOCX files.
- **ATS Match Score:** Combines semantic similarity and keyword gap analysis.
- **AI Feedback:** Qualitative feedback powered by LLMs (OpenAI).
- **PDF Report:** Download a detailed ATS scorecard.
