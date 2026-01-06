"""
Step 2: Raw Data Extraction (PASS 1)
Extracts payroll data AS-IS from PDF text without forcing schema.
Output: interim.json with raw labels and values
"""

import json
import os
from typing import Dict, List
from dotenv import load_dotenv
from anthropic import Anthropic
from src.prompts.extractor_prompt import get_extractor_prompt

# Load environment variables
load_dotenv()


class RawDataExtractor:
    """Extracts raw payroll data from text."""
    
    def __init__(self, model: str = "claude-3-haiku-20240307"):
        """
        Initialize the extractor with Anthropic client.
        
        Args:
            model: Claude model to use (default: Claude 3 Haiku)
        """
        self.api_key = os.getenv("ANTHROPIC_API_KEY")
        
        if not self.api_key:
            raise ValueError(
                "ANTHROPIC_API_KEY not found in environment variables.\n"
                "Please create a .env file with your API key.\n"
                "See .env.example for template."
            )
        
        self.client = Anthropic(api_key=self.api_key)
        self.model = model
    
    def extract_raw_data(self, pages: List[Dict]) -> Dict:
        """
        Extract raw payroll data from pages using Claude.
        
        Args:
            pages: List of page dictionaries with 'page_number' and 'text'
            
        Returns:
            Dictionary with raw extracted payroll data
        """
        # For Haiku with token limitations, process pages individually and combine
        all_employees = []
        report_metadata = None
        
        skipped_pages = []

        for page in pages:
            print(f"Processing page {page['page_number']}...")
            page_text = f"PAGE {page['page_number']}:\n{page['text']}"
            
            prompt = get_extractor_prompt(page_text)
            
            try:
                message = self.client.messages.create(
                    model=self.model,
                    max_tokens=4096,  # Maximum for Haiku model
                    temperature=0,    # No creativity - just extraction
                    messages=[
                        {"role": "user", "content": prompt}
                    ]
                )
                
                # Get the response text
                response_text = message.content[0].text
                
                # Check if response was truncated
                stop_reason = message.stop_reason
                if stop_reason == "max_tokens":
                    print(f"  ⚠ Warning: Page {page['page_number']} response truncated")
                
                # Parse JSON from response
                try:
                    page_result = json.loads(response_text)
                    
                    # Save report metadata from first page
                    if report_metadata is None and page_result.get('report_metadata'):
                        report_metadata = page_result['report_metadata']
                    
                    # Collect employees from this page
                    if page_result.get('employees'):
                        all_employees.extend(page_result['employees'])
                        print(f"  ✓ Extracted {len(page_result['employees'])} employees from page {page['page_number']}")
                    else:
                        print(f"  ⚠ No employees found on page {page['page_number']}")
                        skipped_pages.append(page['page_number'])
                    
                except json.JSONDecodeError as e:
                    print(f"  ✗ Error parsing page {page['page_number']}: {e}")
                    print(f"  Response preview: {response_text[:200]}")
                    # Try JSON repair for this page
                    repaired = self._try_repair_json(response_text, stop_reason)
                    if repaired and repaired.get('employees'):
                        all_employees.extend(repaired['employees'])
                        print(f"  ✓ Recovered {len(repaired['employees'])} employees after repair")
                        if report_metadata is None and repaired.get('report_metadata'):
                            report_metadata = repaired['report_metadata']
                    else:
                        print(f"  ⚠ Skipping page {page['page_number']} due to parsing issues")
                        skipped_pages.append(page['page_number'])
                    
            except Exception as e:
                print(f"  ✗ Error processing page {page['page_number']}: {e}")
                skipped_pages.append(page['page_number'])
                continue
        
        # Combine results
        result = {
            "report_metadata": report_metadata or {},
            "employees": all_employees,
            "skipped_pages": skipped_pages,
        }
        
        print(f"\n✓ Total employees extracted: {len(all_employees)}")
        if skipped_pages:
            print(f"⚠ Pages skipped due to size/parse issues: {skipped_pages}")
        return result
    
    def _try_repair_json(self, text: str, stop_reason: str) -> Dict:
        """Try to repair truncated or malformed JSON."""
        if stop_reason != "max_tokens":
            return None
        
        # Try to fix truncated JSON
        fixed_text = text
        
        # Count brackets to see what needs closing
        open_braces = fixed_text.count('{') - fixed_text.count('}')
        open_brackets = fixed_text.count('[') - fixed_text.count(']')
        
        # Remove any incomplete lines at the end
        lines = fixed_text.split('\n')
        while lines and not lines[-1].strip().endswith((',', '}', ']', '}')):
            lines.pop()
        fixed_text = '\n'.join(lines)
        
        # Remove trailing comma if present
        fixed_text = fixed_text.rstrip().rstrip(',')
        
        # Close arrays and objects
        for _ in range(open_brackets):
            fixed_text += '\n]'
        for _ in range(open_braces):
            fixed_text += '\n}'
        
        try:
            return json.loads(fixed_text)
        except json.JSONDecodeError:
            return None
    
    def validate_interim_format(self, data: Dict) -> bool:
        """
        Validate that the extracted data has expected structure.
        
        Args:
            data: The extracted data dictionary
            
        Returns:
            True if valid, False otherwise
        """
        if not isinstance(data, dict):
            print("✗ Data is not a dictionary")
            return False
        
        if "employees" not in data:
            print("✗ Missing 'employees' key")
            return False
        
        if not isinstance(data["employees"], list):
            print("✗ 'employees' is not a list")
            return False
        
        if len(data["employees"]) == 0:
            print("⚠ Warning: No employees extracted")
            return False
        
        # Check first employee has basic structure
        first_emp = data["employees"][0]
        required_keys = ["employee_name", "earnings", "deductions", "taxes"]
        
        for key in required_keys:
            if key not in first_emp:
                print(f"⚠ Warning: First employee missing key '{key}'")
        
        print(f"✓ Data structure looks valid")
        return True


if __name__ == "__main__":
    # Test extraction
    import sys
    from pathlib import Path
    
    if len(sys.argv) > 1:
        json_file = sys.argv[1]
        
        # Load extracted.json
        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        extractor = RawDataExtractor()
        interim_data = extractor.extract_raw_data(data['pages'])
        
        print("\n" + "="*60)
        print("EXTRACTION SUMMARY")
        print("="*60)
        print(f"Employees extracted: {len(interim_data.get('employees', []))}")
        
        if interim_data.get('employees'):
            emp = interim_data['employees'][0]
            print(f"\nFirst employee: {emp.get('employee_name', 'Unknown')}")
            print(f"  Earnings: {len(emp.get('earnings', []))} lines")
            print(f"  Deductions: {len(emp.get('deductions', []))} lines")
            print(f"  Taxes: {len(emp.get('taxes', []))} lines")
        
        # Save to interim.json
        output_file = Path(json_file).parent / "interim.json"
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(interim_data, f, indent=2, ensure_ascii=False)
        print(f"\n✓ Saved to: {output_file}")
    else:
        print("Usage: python step2_raw_extraction.py <extracted.json>")
