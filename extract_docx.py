
import zipfile
import xml.etree.ElementTree as ET
import sys
import os

def extract_text_from_docx(docx_path):
    try:
        with zipfile.ZipFile(docx_path) as z:
            xml_content = z.read('word/document.xml')
            root = ET.fromstring(xml_content)
            
            # The namespace map for w:
            namespaces = {
                'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'
            }
            
            paragraphs = []
            for p in root.findall('.//w:p', namespaces):
                texts = []
                for node in p.iter():
                    if node.tag.endswith('t'):
                        if node.text:
                            texts.append(node.text)
                    elif node.tag.endswith('tab'):
                        texts.append('\t')
                    elif node.tag.endswith('br') or node.tag.endswith('cr'):
                        texts.append('\n')
                paragraphs.append(''.join(texts))
            
            return '\n'.join(paragraphs)
    except Exception as e:
        return f"Error extracting {docx_path}: {e}"

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python extract_docx.py <file1> [file2 ...]")
        sys.exit(1)
        
    for arg in sys.argv[1:]:
        arg = arg.strip('"').strip("'")
        print(f"\n--- FILE: {arg} ---")
        if os.path.exists(arg):
            try:
                print(extract_text_from_docx(arg))
            except Exception as e:
                print(f"Error: {e}")
        else:
            print(f"File not found: {arg}")
