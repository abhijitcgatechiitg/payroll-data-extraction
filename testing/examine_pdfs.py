"""
Quick script to examine sample PDFs and understand their structure
"""
import pymupdf
from pathlib import Path

def extract_and_display_pdf(pdf_path):
    """Extract and display text from PDF"""
    print("\n" + "="*80)
    print(f"PDF: {pdf_path.name}")
    print("="*80)
    
    doc = pymupdf.open(pdf_path)
    
    for page_num in range(len(doc)):
        page = doc[page_num]
        text = page.get_text()
        
        print(f"\n--- Page {page_num + 1} ---")
        print(text[:2000])  # Show first 2000 chars
        
        if len(text) > 2000:
            print(f"\n... [Truncated, total length: {len(text)} characters] ...")
    
    doc.close()

# Examine all sample PDFs
sample_dir = Path("./sample_pdfs")
pdf_files = list(sample_dir.glob("*.pdf"))

print(f"Found {len(pdf_files)} PDF files")

for pdf_file in pdf_files:
    extract_and_display_pdf(pdf_file)
