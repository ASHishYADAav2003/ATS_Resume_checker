import io
import PyPDF2
import pdfplumber
import docx

def parse_pdf(file_bytes: bytes) -> str:
    """Parse text from a PDF file using pdfplumber as primary, fallback to PyPDF2."""
    text = ""
    try:
        with pdfplumber.open(io.BytesIO(file_bytes)) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
    except Exception as e:
        print(f"pdfplumber failed: {e}. Falling back to PyPDF2.")
        try:
            reader = PyPDF2.PdfReader(io.BytesIO(file_bytes))
            for page in reader.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
        except Exception as fallback_e:
            raise Exception(f"Failed to parse PDF: {fallback_e}")
            
    return text.strip()

def parse_docx(file_bytes: bytes) -> str:
    """Parse text from a DOCX file."""
    try:
        doc = docx.Document(io.BytesIO(file_bytes))
        full_text = []
        for para in doc.paragraphs:
            full_text.append(para.text)
        return "\n".join(full_text).strip()
    except Exception as e:
        raise Exception(f"Failed to parse DOCX: {e}")

def parse_document(filename: str, file_bytes: bytes) -> str:
    """Parse document based on file extension."""
    if filename.lower().endswith('.pdf'):
        return parse_pdf(file_bytes)
    elif filename.lower().endswith('.docx'):
        return parse_docx(file_bytes)
    else:
        raise ValueError(f"Unsupported file format for {filename}")
