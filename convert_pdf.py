import pypdf
import sys

if len(sys.argv) < 2:
    print("Usage: python3 convert_pdf.py <file.pdf>")
    sys.exit(1)

pdf_filename = sys.argv[1]
output_filename = pdf_filename.replace(".pdf", ".txt")

print(f"Reading {pdf_filename}...")

try:
    reader = pypdf.PdfReader(pdf_filename)
    text = ""
    for page in reader.pages:
        text += page.extract_text() + "\n"
    
    with open(output_filename, "w") as f:
        f.write(text)
        
    print(f"Success! Saved to {output_filename}")
except Exception as e:
    print(f"Error: {e}")
