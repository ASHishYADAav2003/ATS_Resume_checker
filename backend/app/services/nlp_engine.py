import spacy
from sentence_transformers import SentenceTransformer, util
import openai
from app.core.config import settings
import json
import logging

logger = logging.getLogger(__name__)

# Load models (this might take a few seconds on first run)
try:
    nlp = spacy.load("en_core_web_sm")
    model = SentenceTransformer('all-MiniLM-L6-v2')
except Exception as e:
    logger.error(f"Failed to load NLP models: {e}")
    # Fallbacks or raise depending on deployment strategy
    nlp = None
    model = None

if settings.OPENAI_API_KEY:
    openai.api_key = settings.OPENAI_API_KEY

def extract_keywords(text: str) -> set:
    """Extract keywords using spaCy noun chunks and entities."""
    if not nlp:
        return set(text.split())
    
    doc = nlp(text)
    keywords = set()
    
    for token in doc:
        if not token.is_stop and not token.is_punct and (token.pos_ == "NOUN" or token.pos_ == "PROPN"):
            keywords.add(token.text.lower())
            
    # Add named entities
    for ent in doc.ents:
        if ent.label_ in ["ORG", "PRODUCT", "WORK_OF_ART"]:
            keywords.add(ent.text.lower())
            
    return keywords

def calculate_similarity(resume_text: str, job_description: str) -> float:
    """Calculate semantic similarity using sentence transformers."""
    if not model:
        return 0.0
    
    embeddings1 = model.encode(resume_text, convert_to_tensor=True)
    embeddings2 = model.encode(job_description, convert_to_tensor=True)
    
    cosine_scores = util.cos_sim(embeddings1, embeddings2)
    return float(cosine_scores[0][0]) * 100

def detect_risks(resume_text: str) -> list:
    """Detect potential risks in the resume."""
    risks = []
    text_lower = resume_text.lower()
    
    if "@" not in text_lower:
        risks.append("Missing email address")
        
    # Basic phone number regex check (very simplified)
    import re
    if not re.search(r'\d{3}[-\.\s]??\d{3}[-\.\s]??\d{4}', text_lower):
        risks.append("Missing phone number")
        
    if len(resume_text.split()) < 100:
        risks.append("Resume is too short")
        
    return risks

async def generate_ai_feedback(resume_text: str, job_description: str) -> dict:
    """Generate qualitative feedback using an LLM."""
    if not settings.OPENAI_API_KEY:
        # Return mock data if API key is not set
        return {
            "strengths": ["Good formatting", "Some relevant keywords present"],
            "weaknesses": ["Lack of quantifiable achievements", "Missing some core technical skills"],
            "suggestions": ["Add more numbers to your experience bullets", "Include specific tools mentioned in the JD"]
        }
    
    prompt = f"""
    You are an expert ATS and recruitment AI. Review the following resume against the job description.
    
    Job Description:
    {job_description[:1500]} # Truncated for token limits
    
    Resume:
    {resume_text[:2000]}
    
    Provide your response strictly in the following JSON format:
    {{
        "strengths": ["strength 1", "strength 2"],
        "weaknesses": ["weakness 1", "weakness 2"],
        "suggestions": ["suggestion 1", "suggestion 2"]
    }}
    """
    
    try:
        response = await openai.ChatCompletion.acreate(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3,
        )
        content = response.choices[0].message.content
        return json.loads(content)
    except Exception as e:
        logger.error(f"Error calling OpenAI API: {e}")
        return {
            "strengths": ["Error generating strengths"],
            "weaknesses": ["Error generating weaknesses"],
            "suggestions": ["Ensure your OpenAI API key is correct and you have quota."]
        }
