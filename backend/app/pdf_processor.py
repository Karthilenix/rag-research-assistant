
import pdfplumber
from io import BytesIO
import traceback

def extract_text_from_pdf(file_bytes: bytes) -> str:
    try:
        text = ""
        with pdfplumber.open(BytesIO(file_bytes)) as pdf:
            for page in pdf.pages:
                # Extracts text with better layout analysis than PyPDF2
                # Extracts text with better layout analysis
                # Increasing tolerance helps with columns and tight text
                page_text = page.extract_text(x_tolerance=3, y_tolerance=3)
                
                # If standard extraction fails (empty), try raw dict extraction or different strategies
                if not page_text or len(page_text.strip()) < 50:
                    print("DEBUG: Standard extraction weak, trying layout=True")
                    page_text = page.extract_text(layout=True)
                
                if page_text:
                    # Basic cleaning: reduce excessive newlines or tabs
                    clean_text = "\n".join([line.strip() for line in page_text.split('\n') if line.strip()])
                    text += clean_text + "\n\n"
        print(f"DEBUG: Extracted text length: {len(text)} characters.")
        if len(text) < 500:
            print(f"DEBUG: Preview: {text[:200]}")
        return text
    except Exception as e:
        print(f"Error extracting PDF text: {e}")
        traceback.print_exc()
        return ""
