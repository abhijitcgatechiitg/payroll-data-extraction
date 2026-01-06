"""
Step 3: Schema Mapping (PASS 2)
Maps raw interim data to global payroll schema using intelligent pattern matching.
Output: mapped.json with structured data following global schema
"""

import json
import os
import copy
import re
from typing import Dict, List, Any, Tuple
from schemas.global_schema import GLOBAL_PAYROLL_SCHEMA, FIELD_ALIASES


class SchemaMatcher:
    """Maps raw payroll data to global schema without LLM (for token efficiency)."""
    
    def __init__(self):
        """Initialize the mapper with field aliases."""
        self.field_aliases = FIELD_ALIASES
    
    def map_interim_to_schema(self, interim_data: Dict) -> Dict:
        """
        Map interim JSON to global schema using pattern matching (no LLM).
        
        Args:
            interim_data: Dictionary with raw extracted data from Step 2
            
        Returns:
            Dictionary following global schema structure with mapped values
        """
        employees = interim_data.get('employees', [])
        
        if not employees:
            print("⚠ Warning: No employees to map")
            return self._create_empty_mapped_schema(interim_data.get('report_metadata', {}))
        
        print(f"Mapping {len(employees)} employees to global schema...")
        
        # Start with global schema template
        output = copy.deepcopy(GLOBAL_PAYROLL_SCHEMA)
        
        # Set metadata
        if interim_data.get('report_metadata'):
            meta = interim_data['report_metadata']
            output['metadata']['report_metadata']['report_title'] = meta.get('report_title')
            output['metadata']['report_metadata']['employer_info']['company_name'] = meta.get('company_name')
            output['metadata']['report_metadata']['employer_info']['company_number'] = meta.get('company_number')
            output['metadata']['report_metadata']['report_period']['period_start_date'] = meta.get('pay_period_start')
            output['metadata']['report_metadata']['report_period']['period_end_date'] = meta.get('pay_period_end')
            output['metadata']['report_metadata']['report_period']['check_date'] = meta.get('check_date')
            output['metadata']['report_metadata']['report_period']['pay_frequency']['value'] = meta.get('pay_frequency')
            output['metadata']['report_metadata']['run_info']['payroll_number'] = meta.get('payroll_number')
            output['metadata']['extraction_timestamp'] = interim_data.get('extraction_timestamp')
        
        # Map employees
        mapped_employees = []
        
        for emp_raw in employees:
            emp_obj = copy.deepcopy(GLOBAL_PAYROLL_SCHEMA['employees'][0])
            
            # Set basic employee info
            emp_obj['employee_info']['employee_name'] = emp_raw.get('employee_name', 'Unknown')
            emp_obj['employee_info']['employee_id'] = emp_raw.get('employee_id', 'Unknown')
            emp_obj['employee_info']['ssn_masked'] = emp_raw.get('ssn_masked')
            emp_obj['employee_info']['department'] = emp_raw.get('department')
            emp_obj['employee_info']['state'] = emp_raw.get('state')
            emp_obj['employee_info']['pay_frequency'] = emp_raw.get('pay_frequency')
            
            # Set tax profile
            if emp_raw.get('tax_status_federal'):
                emp_obj['employee_info']['tax_profile']['federal_filing_status'] = emp_raw.get('tax_status_federal')
                emp_obj['employee_info']['tax_profile']['federal_allowances'] = emp_raw.get('tax_allowances_federal')
            if emp_raw.get('tax_status_state'):
                emp_obj['employee_info']['tax_profile']['state_filing_status'] = emp_raw.get('tax_status_state')
                emp_obj['employee_info']['tax_profile']['state_allowances'] = emp_raw.get('tax_allowances_state')
            
            # Set payment info
            emp_obj['payment_info']['payment_type']['value'] = emp_raw.get('payment_type')
            emp_obj['payment_info']['check_number'] = emp_raw.get('check_number')
            
            # Map earnings with type matching
            emp_obj['earnings']['earning_lines'] = self._map_earning_lines(emp_raw.get('earnings', []))
            
            # Map deductions with type matching
            emp_obj['deductions']['deduction_lines'] = self._map_deduction_lines(emp_raw.get('deductions', []))
            
            # Map taxes with type matching
            emp_obj['employee_taxes']['tax_lines'] = self._map_tax_lines(emp_raw.get('taxes', []))
            
            # Copy totals from raw data
            if emp_raw.get('totals'):
                totals = emp_raw['totals']
                emp_obj['employee_totals']['gross_pay']['current'] = totals.get('gross_pay_current')
                emp_obj['employee_totals']['gross_pay']['ytd'] = totals.get('gross_pay_ytd')
                emp_obj['employee_totals']['total_employee_taxes']['current'] = totals.get('total_taxes_current')
                emp_obj['employee_totals']['total_employee_taxes']['ytd'] = totals.get('total_taxes_ytd')
                emp_obj['employee_totals']['total_deductions']['current'] = totals.get('total_deductions_current')
                emp_obj['employee_totals']['total_deductions']['ytd'] = totals.get('total_deductions_ytd')
                emp_obj['employee_totals']['net_pay']['current'] = totals.get('net_pay_current')
                emp_obj['employee_totals']['net_pay']['ytd'] = totals.get('net_pay_ytd')
            
            mapped_employees.append(emp_obj)
        
        output['employees'] = mapped_employees
        
        # Add skipped pages info if present
        if interim_data.get('skipped_pages'):
            output['metadata']['notes'] = f"Skipped pages due to token limits: {interim_data['skipped_pages']}"
        
        return output
    
    def _map_earning_lines(self, raw_earnings: List[Dict]) -> List[Dict]:
        """Map earning lines with type matching using aliases."""
        earning_lines = []
        
        for raw in raw_earnings:
            desc = raw.get('raw_description', '').lower()
            earning_type = self._match_earning_type(desc)
            
            line = {
                "earning_code": raw.get('raw_code'),
                "earning_description": raw.get('raw_description'),
                "earning_type": {
                    "value": earning_type,
                    "confidence": self._calculate_confidence(desc, earning_type)
                },
                "rate": {
                    "value": raw.get('rate'),
                    "confidence": 1.0 if raw.get('rate') else 0.0
                },
                "hours": {
                    "current": raw.get('hours_current'),
                    "ytd": raw.get('hours_ytd'),
                    "confidence": 1.0 if raw.get('hours_current') else 0.5
                },
                "amount": {
                    "current": raw.get('amount_current'),
                    "ytd": raw.get('amount_ytd'),
                    "confidence": 1.0 if raw.get('amount_current') else 0.0
                },
                "notes": ""
            }
            earning_lines.append(line)
        
        return earning_lines
    
    def _map_deduction_lines(self, raw_deductions: List[Dict]) -> List[Dict]:
        """Map deduction lines with type matching using aliases."""
        deduction_lines = []
        
        for raw in raw_deductions:
            desc = raw.get('raw_description', '').lower()
            ded_type = self._match_deduction_type(desc)
            
            line = {
                "deduction_code": raw.get('raw_code'),
                "deduction_description": raw.get('raw_description'),
                "deduction_type": {
                    "value": ded_type,
                    "confidence": self._calculate_confidence(desc, ded_type)
                },
                "is_pre_tax": {
                    "value": self._is_pre_tax(ded_type),
                    "confidence": 0.95
                },
                "amount": {
                    "current": raw.get('amount_current'),
                    "ytd": raw.get('amount_ytd'),
                    "confidence": 1.0 if raw.get('amount_current') else 0.0
                },
                "notes": ""
            }
            deduction_lines.append(line)
        
        return deduction_lines
    
    def _map_tax_lines(self, raw_taxes: List[Dict]) -> List[Dict]:
        """Map tax lines with type matching using aliases."""
        tax_lines = []
        
        for raw in raw_taxes:
            desc = raw.get('raw_description', '').lower()
            tax_type, authority, jurisdiction = self._match_tax_type(desc)
            
            line = {
                "tax_code": raw.get('raw_code'),
                "tax_description": raw.get('raw_description'),
                "tax_type": {
                    "value": tax_type,
                    "confidence": self._calculate_confidence(desc, tax_type)
                },
                "tax_authority": {
                    "value": authority,
                    "confidence": 0.95 if authority else 0.5
                },
                "jurisdiction": jurisdiction,
                "tax_amount": {
                    "current": raw.get('amount_current'),
                    "ytd": raw.get('amount_ytd'),
                    "confidence": 1.0 if raw.get('amount_current') else 0.0
                },
                "notes": ""
            }
            tax_lines.append(line)
        
        return tax_lines
    
    def _match_earning_type(self, description: str) -> str:
        """Match earning description to normalized type."""
        aliases = self.field_aliases.get('earning_types', {})
        
        for normalized_type, patterns in aliases.items():
            for pattern in patterns:
                if pattern.lower() in description:
                    return normalized_type
        
        return "Other"
    
    def _match_deduction_type(self, description: str) -> str:
        """Match deduction description to normalized type."""
        aliases = self.field_aliases.get('deduction_types', {})
        
        for normalized_type, patterns in aliases.items():
            for pattern in patterns:
                if pattern.lower() in description:
                    return normalized_type
        
        return "Other"
    
    def _match_tax_type(self, description: str) -> Tuple[str, str, str]:
        """Match tax description to normalized type, authority, and jurisdiction."""
        aliases = self.field_aliases.get('tax_types', {})
        
        tax_type = "Other"
        authority = "Federal"
        jurisdiction = None
        
        # Check for jurisdiction first
        jurisdiction_patterns = ["ma:", "ca:", "ny:", "tx:", "fl:"]
        for pattern in jurisdiction_patterns:
            if pattern in description:
                jurisdiction = pattern.replace(":", "").upper()
                authority = "State"
                break
        
        # Match tax type
        for normalized_type, patterns in aliases.items():
            for pattern in patterns:
                if pattern.lower() in description:
                    tax_type = normalized_type
                    # Determine authority based on type
                    if "federal" in normalized_type.lower() or "fica" in normalized_type.lower():
                        authority = "Federal"
                    elif "state" in normalized_type.lower() or "sdi" in normalized_type.lower() or "sui" in normalized_type.lower():
                        authority = "State"
                    elif "local" in normalized_type.lower():
                        authority = "Local"
                    return tax_type, authority, jurisdiction
        
        return tax_type, authority, jurisdiction
    
    def _is_pre_tax(self, deduction_type: str) -> bool:
        """Determine if deduction is pre-tax."""
        pre_tax_types = ["401k", "403b", "fsa", "hsa"]
        return any(pt in deduction_type.lower() for pt in pre_tax_types)
    
    def _calculate_confidence(self, description: str, matched_type: str) -> float:
        """Calculate confidence score for match."""
        if matched_type == "Other":
            return 0.3  # Low confidence for "Other"
        return 0.85  # High confidence for matched types
    
    def _create_empty_mapped_schema(self, report_metadata: Dict) -> Dict:
        """Create empty schema with metadata."""
        output = copy.deepcopy(GLOBAL_PAYROLL_SCHEMA)
        output['metadata']['report_metadata'] = report_metadata
        return output


if __name__ == "__main__":
    # Test mapping
    import sys
    from pathlib import Path
    
    if len(sys.argv) > 1:
        json_file = sys.argv[1]
        
        # Load interim.json
        with open(json_file, 'r', encoding='utf-8') as f:
            interim_data = json.load(f)
        
        matcher = SchemaMatcher()
        mapped_data = matcher.map_interim_to_schema(interim_data)
        
        print("\n" + "="*60)
        print("MAPPING SUMMARY")
        print("="*60)
        print(f"Employees mapped: {len(mapped_data.get('employees', []))}")
        
        # Save to mapped.json
        output_file = Path(json_file).parent / "mapped.json"
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(mapped_data, f, indent=2, ensure_ascii=False)
        print(f"\n✓ Saved to: {output_file}")
    else:
        print("Usage: python step3_schema_mapping.py <interim.json>")
