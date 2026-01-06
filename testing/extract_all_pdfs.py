"""
Extract complete text from sample PDFs
"""
import pymupdf
from pathlib import Path
import json

def extract_complete_pdf(pdf_path):
    """Extract complete text from PDF"""
    doc = pymupdf.open(pdf_path)
    
    pages_data = []
    for page_num in range(len(doc)):
        page = doc[page_num]
        text = page.get_text()
        pages_data.append({
            'page_number': page_num + 1,
            'text': text
        })
    
    doc.close()
    return pages_data

# Extract all sample PDFs
sample_dir = Path("./sample_pdfs")
pdf_files = list(sample_dir.glob("*.pdf"))

for pdf_file in pdf_files:
    print(f"\n{'='*80}")
    print(f"Extracting: {pdf_file.name}")
    print('='*80)
    
    pages = extract_complete_pdf(pdf_file)
    
    # Save to JSON
    output_file = f"pdf_text_{pdf_file.stem}.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump({
            'filename': pdf_file.name,
            'pages': pages
        }, f, indent=2, ensure_ascii=False)
    
    print(f"Extracted {len(pages)} pages")
    print(f"Saved to: {output_file}")
    
    # Show first page
    if pages:
        print(f"\n--- First Page Preview ---")
        print(pages[0]['text'][:1500])
