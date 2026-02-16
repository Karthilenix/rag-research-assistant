
import pdfplumber
from io import BytesIO
import traceback

def extract_text_from_pdf(file_bytes: bytes) -> str:
    try:
        text = ""
        with pdfplumber.open(BytesIO(file_bytes)) as pdf:
            for page in pdf.pages:
                # Extracts text with better layout analysis than PyPDF2
                page_text = page.extract_text(x_tolerance=2, y_tolerance=2)
                if page_text:
                    text += page_text + "\n"
        print(f"DEBUG: Extracted text length: {len(text)} characters.")
        if len(text) < 500:
            print(f"DEBUG: Preview: {text[:200]}")
        return text
    except Exception as e:
        print(f"Error extracting PDF text: {e}")
        traceback.print_exc()
        return ""
