"""
Main Orchestrator for Payroll Data Extraction
Runs the entire pipeline from PDF to structured JSON output.

Usage: python main.py <pdf_filename>
Example: python main.py PR-Register.pdf
"""

import sys
import json
from pathlib import Path
from datetime import datetime

# Import pipeline steps
from src.step1_pdf_extraction import extract_text_from_pdf
from src.step2_raw_extraction import RawDataExtractor
from src.step3_schema_mapping import SchemaMatcher
# TODO: Import remaining steps after implementation
# from src.step4_validation import PayrollValidator


def log_step(step_num: int, step_name: str):
    """Print formatted step header."""
    print("\n" + "="*60)
    print(f"STEP {step_num}: {step_name}")
    print("="*60)


def log_success(message: str):
    """Print success message."""
    print(f"✓ {message}")


def log_error(message: str):
    """Print error message."""
    print(f"✗ {message}")


def ensure_output_dir(pdf_name: str) -> Path:
    """Create and return the output directory for a PDF."""
    output_dir = Path("./outputs") / pdf_name
    output_dir.mkdir(parents=True, exist_ok=True)
    return output_dir


def main():
    """Main orchestration function."""
    
    # Parse command line arguments
    if len(sys.argv) < 2:
        print("Usage: python main.py <pdf_filename>")
        print("Example: python main.py PR-Register.pdf")
        print("\nAvailable PDFs in sample_pdfs/:")
        sample_pdfs = list(Path("./sample_pdfs").glob("*.pdf"))
        for pdf in sample_pdfs:
            print(f"  - {pdf.name}")
        sys.exit(1)
    
    pdf_filename = sys.argv[1]
    
    # Handle both full path and just filename
    if Path(pdf_filename).exists():
        pdf_path = pdf_filename
    else:
        pdf_path = f"./sample_pdfs/{pdf_filename}"
    
    # Verify PDF exists
    if not Path(pdf_path).exists():
        log_error(f"PDF file not found: {pdf_path}")
        sys.exit(1)
    
    base_name = Path(pdf_filename).stem
    
    # Create output directory for this PDF
    output_dir = ensure_output_dir(base_name)
    
    print("\n" + "="*60)
    print("PAYROLL DATA EXTRACTION PIPELINE")
    print("="*60)
    print(f"Processing: {pdf_filename}")
    print(f"Output directory: {output_dir}")
    print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    try:
        # ==========================================
        # STEP 1: Extract text from PDF
        # ==========================================
        log_step(1, "PDF Text Extraction")
        
        pages = extract_text_from_pdf(pdf_path)
        
        if not pages:
            log_error("No pages extracted from PDF")
            sys.exit(1)
        
        log_success(f"Extracted {len(pages)} pages from PDF")
        
        # Save extracted pages
        extracted_json_path = output_dir / "extracted.json"
        with open(extracted_json_path, 'w', encoding='utf-8') as f:
            json.dump({
                "source_file": pdf_filename,
                "extraction_timestamp": datetime.now().isoformat(),
                "total_pages": len(pages),
                "pages": pages
            }, f, indent=2, ensure_ascii=False)
        log_success(f"Saved to: {extracted_json_path}")
        
        # Print page preview
        print("\n  Page previews:")
        for page in pages[:3]:  # Show first 3 pages
            text_preview = page['text'][:80].replace('\n', ' ')
            print(f"    Page {page['page_number']}: {text_preview}...")
        
        if len(pages) > 3:
            print(f"    ... and {len(pages) - 3} more pages")
        
        # ==========================================
        # STEP 2: Raw extraction (PASS 1)
        # ==========================================
        log_step(2, "Raw Data Extraction (PASS 1)")
        
        extractor = RawDataExtractor()
        interim_data = extractor.extract_raw_data(pages)
        
        # Validate interim format
        if not extractor.validate_interim_format(interim_data):
            print("⚠ Warning: Extracted data may not have expected format")
            print("  Continuing anyway...")
        
        log_success(f"Extracted data for {len(interim_data.get('employees', []))} employees")
        
        # Show extraction summary
        if interim_data.get('report_metadata'):
            meta = interim_data['report_metadata']
            print(f"\n  Report: {meta.get('report_title', 'Unknown')}")
            print(f"  Company: {meta.get('company_name', 'Unknown')}")
            print(f"  Pay Period: {meta.get('pay_period_start', '?')} to {meta.get('pay_period_end', '?')}")
        
        if interim_data.get('employees'):
            print(f"\n  Sample employee (first):")
            emp = interim_data['employees'][0]
            print(f"    Name: {emp.get('employee_name', 'Unknown')}")
            print(f"    ID: {emp.get('employee_id', 'Unknown')}")
            print(f"    Earnings: {len(emp.get('earnings', []))} lines")
            print(f"    Deductions: {len(emp.get('deductions', []))} lines")
            print(f"    Taxes: {len(emp.get('taxes', []))} lines")
        
        # Save interim JSON
        interim_json_path = output_dir / "interim.json"
        with open(interim_json_path, 'w', encoding='utf-8') as f:
            json.dump(interim_data, f, indent=2, ensure_ascii=False)
        log_success(f"Saved to: {interim_json_path}")
        
        # ==========================================
        # STEP 3: Schema mapping (PASS 2)
        # ==========================================
        log_step(3, "Schema Mapping (PASS 2)")
        
        matcher = SchemaMatcher()
        mapped_data = matcher.map_interim_to_schema(interim_data)
        
        log_success(f"Mapped {len(mapped_data.get('employees', []))} employees to global schema")
        
        # Show mapping summary
        if mapped_data.get('employees'):
            print(f"\n  Sample mapped employee:")
            emp = mapped_data['employees'][0]
            print(f"    Name: {emp['employee_info'].get('employee_name', 'Unknown')}")
            print(f"    Earnings types: {len(emp.get('earnings', {}).get('earning_lines', []))} mapped")
            print(f"    Deduction types: {len(emp.get('deductions', {}).get('deduction_lines', []))} mapped")
            print(f"    Tax types: {len(emp.get('employee_taxes', {}).get('tax_lines', []))} mapped")
        
        # Save mapped JSON
        mapped_json_path = output_dir / "mapped.json"
        with open(mapped_json_path, 'w', encoding='utf-8') as f:
            json.dump(mapped_data, f, indent=2, ensure_ascii=False)
        log_success(f"Saved to: {mapped_json_path}")
        
        # ==========================================
        # TODO: STEP 4: Validation
        # ==========================================
        print("\n" + "="*60)
        print("Step 4: Coming next...")
        print("="*60)
        print("\n✓ Steps 1-3 completed successfully!")
        print(f"✓ Output saved to: {output_dir}/")
        
    except Exception as e:
        log_error(f"Pipeline failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
