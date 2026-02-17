
import pdfplumber
import sys
import os

def debug_pdf(file_path):
    print(f"--- Processing {file_path} ---")
    if not os.path.exists(file_path):
        print("File not found.")
        return

    try:
        with pdfplumber.open(file_path) as pdf:
            full_text = ""
            for i, page in enumerate(pdf.pages):
                print(f"--- Page {i+1} ---")
                # Try default extraction
                text = page.extract_text()
                if text:
                    print(f"[Default Extraction]:\n{text[:500]}...\n")
                    full_text += text
                else:
                    print("[Default Extraction Failed or Empty]")
                    
                # Try layout extraction
                text_layout = page.extract_text(layout=True)
                if text_layout:
                    print(f"[Layout Extraction]:\n{text_layout[:500]}...\n")
                
            print("-" * 30)
            print("Full Text Search Check:")
            if "PROJECTS" in full_text.upper():
                print("✅ Found 'PROJECTS' section header.")
            else:
                print("❌ 'PROJECTS' header NOT found in extracted text.")
                
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python debug_pdf.py <path_to_pdf>")
    else:
        debug_pdf(sys.argv[1])
