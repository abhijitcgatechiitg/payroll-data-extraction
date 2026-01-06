# Schema Mapping Example - PR-Register.pdf

This document shows how data from the sample PDF maps to our global schema.

## Sample Employee Data from PDF

```
Employee: Golikowski, Roger D.
Emp. No.: 2001015
SSN: *******6132
Dept: 1
Pay Freq: Weekly
Tax Status: Fed: Married 0, MA: Married 0
Type: DD (Direct Deposit)
Ck. No.: 26

Earnings:
  0-Regular Pay: Rate 19.75, Hours 40.00 Current, 280.00 YTD
                 Amount: $790.00 Current, $5,530.00 YTD

Deductions:
  4-401K Plan: $23.70 Current, $165.90 YTD

Taxes:
  Federal WH: $511.84 Current, $73.12 YTD (seems reversed in PDF)
  OASDI: $342.86 Current, $48.98 YTD
  Medicare: $80.19 Current, $11.45 YTD
  MA: State WH: $256.93 Current, $36.71 YTD

Net Pay: $596.04
```

## How This Maps to Schema

```python
{
  "employees": [
    {
      "employee_info": {
        "employee_name": "Golikowski, Roger D.",
        "employee_id": "2001015",
        "ssn_masked": "*******6132",
        "department": "1",
        "state": "MA",
        "pay_frequency": "Weekly",
        "tax_profile": {
          "federal_filing_status": "Married",
          "federal_allowances": 0,
          "state_filing_status": "Married",
          "state_allowances": 0
        }
      },
      
      "payment_info": {
        "payment_type": {
          "value": "Direct Deposit",
          "confidence": 1.0
        },
        "check_number": "26"
      },
      
      "earnings": {
        "earning_lines": [
          {
            "earning_code": "0",
            "earning_description": "Regular Pay",
            "earning_type": {
              "value": "Regular Pay",
              "confidence": 1.0
            },
            "rate": {
              "value": 19.75,
              "confidence": 1.0
            },
            "hours": {
              "current": 40.00,
              "ytd": 280.00,
              "confidence": 1.0
            },
            "amount": {
              "current": 790.00,
              "ytd": 5530.00,
              "confidence": 1.0
            }
          }
        ],
        "earnings_totals": {
          "gross_pay": {
            "current": 790.00,
            "ytd": 5530.00,
            "confidence": 1.0
          },
          "total_hours": {
            "current": 40.00,
            "ytd": 280.00,
            "confidence": 1.0
          }
        }
      },
      
      "employee_taxes": {
        "tax_lines": [
          {
            "tax_code": None,
            "tax_description": "Federal WH",
            "tax_type": {
              "value": "Federal WH",
              "confidence": 1.0
            },
            "tax_authority": {
              "value": "Federal",
              "confidence": 1.0
            },
            "jurisdiction": None,
            "tax_amount": {
              "current": 73.12,
              "ytd": 511.84,
              "confidence": 0.9  # Note: Values appear swapped in PDF
            }
          },
          {
            "tax_description": "OASDI",
            "tax_type": {
              "value": "OASDI",
              "confidence": 1.0
            },
            "tax_authority": {
              "value": "Federal",
              "confidence": 1.0
            },
            "tax_amount": {
              "current": 48.98,
              "ytd": 342.86,
              "confidence": 0.9
            }
          },
          {
            "tax_description": "Medicare",
            "tax_type": {
              "value": "Medicare",
              "confidence": 1.0
            },
            "tax_authority": {
              "value": "Federal",
              "confidence": 1.0
            },
            "tax_amount": {
              "current": 11.45,
              "ytd": 80.19,
              "confidence": 0.9
            }
          },
          {
            "tax_description": "MA: State WH",
            "tax_type": {
              "value": "State WH",
              "confidence": 1.0
            },
            "tax_authority": {
              "value": "State",
              "confidence": 1.0
            },
            "jurisdiction": "MA",
            "tax_amount": {
              "current": 36.71,
              "ytd": 256.93,
              "confidence": 0.9
            }
          }
        ],
        "employee_tax_totals": {
          "total_employee_taxes": {
            "current": 170.26,  # Sum of all tax current values
            "ytd": 1190.82,     # Sum of all tax YTD values
            "confidence": 0.95
          }
        }
      },
      
      "deductions": {
        "deduction_lines": [
          {
            "deduction_code": "4",
            "deduction_description": "401K Plan",
            "deduction_type": {
              "value": "Retirement - 401k",
              "confidence": 1.0
            },
            "is_pre_tax": {
              "value": True,
              "confidence": 1.0
            },
            "amount": {
              "current": 23.70,
              "ytd": 165.90,
              "confidence": 1.0
            }
          }
        ],
        "deductions_totals": {
          "total_deductions": {
            "current": 23.70,
            "ytd": 165.90,
            "confidence": 1.0
          }
        }
      },
      
      "net_pay": {
        "net_amount": {
          "current": 596.04,
          "ytd": None,  # Not shown in this format
          "confidence": 1.0
        }
      },
      
      "employee_totals": {
        "gross_pay": {
          "current": 790.00,
          "ytd": 5530.00,
          "confidence": 1.0
        },
        "total_employee_taxes": {
          "current": 170.26,
          "ytd": None,
          "confidence": 0.95
        },
        "total_deductions": {
          "current": 23.70,
          "ytd": 165.90,
          "confidence": 1.0
        },
        "net_pay": {
          "current": 596.04,
          "ytd": None,
          "confidence": 1.0
        }
      }
    }
  ]
}
```

## Report Metadata Mapping

From the PDF footer:
```
Pay Period: 03/23/14 - 03/29/14
Check Date: 04/04/14
PAYROLL REGISTER
Co. No: 99
Payroll #: 198
The Sample Company
Page: 1
```

Maps to:
```python
{
  "metadata": {
    "report_metadata": {
      "report_title": "PAYROLL REGISTER",
      "report_type": {
        "value": "Payroll Register",
        "confidence": 1.0
      },
      "employer_info": {
        "company_name": "The Sample Company",
        "company_number": "99"
      },
      "report_period": {
        "pay_frequency": {
          "value": "Weekly",
          "confidence": 1.0
        },
        "period_start_date": "2014-03-23",
        "period_end_date": "2014-03-29",
        "check_date": "2014-04-04"
      },
      "run_info": {
        "payroll_number": "198"
      },
      "document_refs": {
        "page_number": 1,
        "total_pages": 2
      }
    }
  }
}
```

## Interesting Cases from PDF

### Employee with Multiple Earning Types (Jonathon Bird)
```
Employee: Bird, Jonathon
Earnings:
  0-Regular Pay: Rate 23.50, Hours 40.00, Amount $940.00 Current, $5,640.00 YTD
  1-Vacation Pay: Hours 40.00, Amount $940.00 YTD only
  
Total Current: $940.00
Total YTD: $6,580.00 (includes both)
```

This shows vacation was taken in previous periods, not current.

### Employee with Child Support Garnishment (Kevin McCue)
```
Deductions:
  2-CAF Medical: $72.69 Current, $508.83 YTD
  31-Child Support: $350.10 Current, $2,100.61 YTD  <-- Large garnishment
```

### Employee with Bonus (William Sample)
```
Earnings:
  0-Regular Pay: $0.00 Current, $25,550.00 YTD
  3-Bonus Pay: $2,800.00 Current, $25,200.00 YTD
  
Total: $6,450.00 Current (some calculations seem off in PDF)
```

This is a salaried employee getting a bonus.

### Employee with Employer Match Memo (Rick Fournier)
```
Deductions:
  4-401K Plan: $33.50 Current, $201.00 YTD
  M2-401(k) ER M: $6.70 Current, $40.20 YTD  <-- Employer match (memo only)
```

The "M2" indicates it's a memo (informational) showing employer contribution.

## Validation Rules Based on Sample

1. **Gross Pay Calculation**: `Sum of all earning amounts = Gross Pay`
2. **Net Pay Calculation**: `Gross Pay - Total Taxes - Total Deductions = Net Pay`
3. **Hours Validation**: `Hours * Rate = Amount` (for hourly employees)
4. **YTD >= Current**: YTD values should always be >= current period values
5. **Tax Percentages**: 
   - OASDI ≈ 6.2% of gross
   - Medicare ≈ 1.45% of gross
   - Federal WH varies by filing status

## Notes on PDF Quirks

1. **Current/YTD may be swapped** in some columns (see Federal WH)
2. **Negative values** can appear for adjustments (see Bergeron, Patrick: sick pay adjustment)
3. **Memo items** (like M2-401(k) ER M) should not affect net pay calculations
4. **Multiple pages** require aggregation across pages
5. **Department totals** are not shown in this specific PDF but schema supports them

---

This mapping example demonstrates that our schema can accommodate all data elements from the actual payroll register PDF.
