"""
Step 1: PDF Text Extraction
Extracts text from payroll PDF using PyMuPDF.
Output: pages with text content
"""

import pymupdf
from pathlib import Path
from typing import List, Dict


def extract_text_from_pdf(pdf_path: str) -> List[Dict]:
    """
    Extract text from each page of a PDF file.
    
    Args:
        pdf_path: Path to the PDF file
        
    Returns:
        List of dictionaries with page_number and text for each page
        
    Example:
        [
            {"page_number": 1, "text": "Page 1 content..."},
            {"page_number": 2, "text": "Page 2 content..."}
        ]
    """
    pdf_path = Path(pdf_path)
    
    if not pdf_path.exists():
        raise FileNotFoundError(f"PDF file not found: {pdf_path}")
    
    if not pdf_path.suffix.lower() == '.pdf':
        raise ValueError(f"File must be a PDF: {pdf_path}")
    
    pages = []
    
    try:
        # Open PDF with PyMuPDF
        doc = pymupdf.open(pdf_path)
        
        # Extract text from each page
        for page_num in range(len(doc)):
            page = doc[page_num]
            text = page.get_text()
            
            pages.append({
                "page_number": page_num + 1,
                "text": text
            })
        
        doc.close()
        
        print(f"Successfully extracted {len(pages)} pages from {pdf_path.name}")
        
        return pages
        
    except Exception as e:
        raise Exception(f"Error extracting text from PDF: {e}")


if __name__ == "__main__":
    # Test extraction
    import sys
    if len(sys.argv) > 1:
        pdf_file = sys.argv[1]
        pages = extract_text_from_pdf(pdf_file)
        print(f"\nExtracted {len(pages)} pages")
        if pages:
            print(f"\nFirst page preview (first 200 chars):")
            print(pages[0]['text'][:200])
    else:
        print("Usage: python step1_pdf_extraction.py <pdf_file>")
