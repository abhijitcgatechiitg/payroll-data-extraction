# Global Payroll Schema - Summary & Changes

## Overview
The new [global_schema.py](schemas/global_schema.py) is a comprehensive Python dictionary that represents the universal structure for payroll data extraction. It's designed to handle various payroll report formats while maintaining consistency.

## Key Improvements from v2

### 1. **Format Change**
- ✅ **Converted from JSON to Python dict** (matches old financial project structure)
- ✅ Added as a constant `GLOBAL_PAYROLL_SCHEMA` that can be imported

### 2. **Enhanced Employee Classification**
Added new fields for better employee categorization:
```python
"employment_type": {
    "allowed_values": ["Full-Time", "Part-Time", "Contractor", "Temporary", "Seasonal", "Other"]
}

"pay_type": {
    "allowed_values": ["Hourly", "Salaried", "Other"]
}
```

### 3. **Expanded Earning Types**
Based on sample PDF analysis, added common earning types:
- Regular Pay
- Overtime / Double Time
- Vacation Pay / Sick Pay / Holiday Pay
- Bonus / Commission
- Severance / Retroactive Pay

Each earning line now includes:
- `earning_code` (e.g., "0", "1", "REG")
- `earning_type` with normalized classification
- `taxable_flags` for tax applicability

### 4. **Comprehensive Tax Handling**
Enhanced tax structure with:
```python
"tax_type": {
    "allowed_values": [
        "Federal Income Tax",
        "Federal WH",
        "OASDI",      # Social Security
        "Medicare",
        "State Income Tax",
        "State WH",
        "Local Income Tax",
        "SDI",        # State Disability Insurance
        "SUI",        # State Unemployment Insurance
        "Other"
    ]
}

"jurisdiction": None  # e.g., "MA", "CA", "NYC" for state/local taxes
```

### 5. **Detailed Deduction Categories**
Expanded deduction types based on real payroll data:
- Retirement plans (401k, 403b, IRA)
- Insurance (Health, Dental, Vision, Life, Disability)
- Pre-tax accounts (FSA, HSA)
- Garnishments (Child Support, Tax Levy)
- Union Dues, Loan Repayments
- Memo-only items

Added `is_pre_tax` flag to track pre-tax vs post-tax deductions.

### 6. **Enhanced Report Metadata**
Added fields found in actual payroll reports:
```python
"company_number": None      # Co. No.
"payroll_number": None      # Payroll run number
"pay_frequency": {...}      # Weekly, Biweekly, etc.
```

### 7. **Payment Information**
Enhanced payment tracking:
- Payment type (Check, Direct Deposit/DD, Cash)
- Check number
- Bank account (masked)
- Pay date

### 8. **Employer Tax Support**
Added section for employer-paid taxes (often in summary reports):
```python
"employer_taxes": {
    "tax_lines": [
        {
            "tax_type": {
                "allowed_values": [
                    "Employer FICA",
                    "Employer Medicare",
                    "FUTA",  # Federal Unemployment Tax
                    "SUTA",  # State Unemployment Tax
                    "Workers Comp",
                    "Other"
                ]
            }
        }
    ]
}
```

### 9. **Comprehensive Rollup Structure**
Enhanced company totals with:
- Employee count
- Earning breakdowns by type
- Tax breakdowns by authority
- Deduction breakdowns by category

### 10. **Field Aliases Dictionary**
Added `FIELD_ALIASES` dictionary at the bottom for mapping:
```python
FIELD_ALIASES = {
    "earnings": {
        "Regular Pay": ["Regular", "Reg Pay", "0-Regular Pay", "REG"],
        "Vacation Pay": ["Vacation", "1-Vacation Pay", "VAC", "PTO"],
        # ... more aliases
    },
    "taxes": {
        "Federal Income Tax": ["Federal WH", "FWT", "Fed WH"],
        "OASDI": ["OASDI", "Social Security", "SS"],
        # ... more aliases
    },
    # ... deductions, payment types, pay frequencies
}
```

This will be used in Pass 2 to intelligently map raw labels to normalized types.

## Schema Structure

```
GLOBAL_PAYROLL_SCHEMA
├── metadata
│   ├── currency
│   └── report_metadata
│       ├── report_type
│       ├── employer_info
│       ├── report_period
│       ├── run_info
│       └── document_refs
├── employees[] (array of employee objects)
│   ├── employee_info
│   │   ├── Basic info (name, ID, SSN)
│   │   ├── Classification (dept, location, state)
│   │   ├── employment_type
│   │   ├── pay_type
│   │   └── tax_profile
│   ├── payment_info
│   ├── earnings
│   │   ├── earning_lines[]
│   │   └── earnings_totals
│   ├── employee_taxes
│   │   ├── tax_lines[]
│   │   └── employee_tax_totals
│   ├── deductions
│   │   ├── deduction_lines[]
│   │   └── deductions_totals
│   ├── net_pay
│   └── employee_totals
└── rollups
    ├── department_totals[]
    └── company_totals
        ├── earnings_totals
        ├── employee_withholding_totals
        ├── employer_taxes
        ├── deduction_totals
        └── grand_totals
```

## Sample PDF Analysis

Based on **PR-Register.pdf**:
- ✅ Multiple employees per page
- ✅ Employee info: Name, Emp. No., SSN (masked), Dept., Tax Status
- ✅ Earnings: "0-Regular Pay" with rate, hours, current, YTD
- ✅ Deductions: "4-401K Plan", "2-CAF Medical", "31-Child Support"
- ✅ Taxes: "Federal WH", "OASDI", "Medicare", "MA: State WH"
- ✅ Payment: Check number, Type (DD = Direct Deposit)
- ✅ Both Current and YTD values throughout
- ✅ Report header: Pay Period, Check Date, Payroll #, Company Name

**All elements from the sample are covered in the schema!**

## Next Steps

1. ✅ Schema finalized in Python dict format
2. ⏭️ Create project structure (main.py, src/, prompts/)
3. ⏭️ Write Pass 1 prompt (raw extraction)
4. ⏭️ Write Pass 2 prompt (schema mapping)
5. ⏭️ Implement validation logic
6. ⏭️ Test with sample PDFs

## Notes

- Schema supports partial data - all fields are optional (None by default)
- Confidence scores throughout for quality tracking
- Notes fields for capturing additional context
- Designed to handle variations across payroll systems
- Flexible enough for different report types while maintaining structure
