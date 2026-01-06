{
  "section": "PayrollRegister",
  "metadata": {
    "description": "Payroll register / employee earnings and taxes report",
    "source_filename": null,
    "extraction_timestamp": null,

    "currency": {
      "description": "Currency used in the report if detectable (e.g., USD). If not, set null.",
      "code": null,
      "symbol": null,
      "confidence": 0.0
    },

    "report_metadata": {
      "description": "High-level report header details found at the top of the PDF.",
      "report_title": null,
      "report_type": {
        "description": "Normalized type classification for payroll PDFs.",
        "value": null,
        "allowed_values": [
          "Payroll Register",
          "Employee Earnings and Taxes",
          "Payroll Summary",
          "Other"
        ],
        "confidence": 0.0
      },

      "employer_info": {
        "description": "Employer/company information shown in report header.",
        "company_name": null,
        "company_id": null,
        "address": null,
        "worksite_or_location": null,
        "notes": ""
      },

      "report_period": {
        "description": "Pay cycle coverage. Often a pay period start/end and a check date.",
        "pay_frequency": {
          "value": null,
          "allowed_values": ["Weekly", "Biweekly", "Semi-Monthly", "Monthly", "Other"],
          "confidence": 0.0
        },
        "period_start_date": null,
        "period_end_date": null,
        "check_date": null
      },

      "run_info": {
        "description": "Run or print metadata such as generated timestamp.",
        "generated_datetime": null,
        "generated_by": null,
        "system_name": null
      },

      "document_refs": {
        "description": "Document identifiers like payroll number, page number, batch/run id.",
        "payroll_number": null,
        "batch_id": null,
        "page_number": null,
        "total_pages": null
      }
    }
  },

  "employees": [
    {
      "employee_info": {
        "description": "Employee identity and context fields.",
        "employee_name": null,
        "employee_id": null,
        "ssn_masked": null,

        "department": null,
        "location": null,
        "state": null,

        "pay_frequency": null,
        "job_title": null,

        "tax_profile": {
          "description": "Filing/tax setup if present (often federal/state status and allowances).",
          "federal_filing_status": null,
          "federal_allowances": null,
          "state_filing_status": null,
          "state_allowances": null,
          "additional_withholding": null
        },

        "notes": ""
      },

      "payment_info": {
        "description": "How the employee was paid for this payroll run.",
        "payment_type": {
          "value": null,
          "allowed_values": ["Check", "Direct Deposit", "Cash", "Other"],
          "confidence": 0.0
        },
        "check_number": null,
        "bank_account_masked": null,
        "pay_date": null
      },

      "earnings": {
        "description": "Earnings lines such as Regular, Overtime, Bonus, Vacation, etc.",
        "earning_lines": [
          {
            "description": "One earning type line item.",
            "earning_code": null,
            "earning_description": null,

            "rate": {
              "description": "Hourly rate or pay rate if shown.",
              "value": null,
              "confidence": 0.0
            },

            "hours": {
              "description": "Hours for this earning line if shown.",
              "current": null,
              "ytd": null,
              "confidence": 0.0
            },

            "amount": {
              "description": "Amount paid for this earning line.",
              "current": null,
              "ytd": null,
              "confidence": 0.0
            },

            "taxable_flags": {
              "description": "If the report indicates whether this earning is taxable for certain taxes.",
              "federal_taxable": null,
              "fica_taxable": null,
              "state_taxable": null
            },

            "notes": ""
          }
        ],

        "earnings_totals": {
          "description": "Totals of all earnings for the employee.",
          "gross_pay": {
            "current": null,
            "ytd": null,
            "confidence": 0.0
          },
          "total_hours": {
            "current": null,
            "ytd": null,
            "confidence": 0.0
          },
          "notes": ""
        }
      },

      "balance_employee_tax": {
        "description": "Employee withholding taxes (employee-paid).",
        "tax_lines": [
          {
            "tax_code": null,
            "tax_description": null,
            "tax_authority": {
              "description": "Optional normalized authority label if detectable.",
              "value": null,
              "allowed_values": ["Federal", "State", "Local", "Other"],
              "confidence": 0.0
            },
            "tax_amount": {
              "current": null,
              "ytd": null,
              "confidence": 0.0
            },
            "notes": ""
          }
        ],

        "employee_tax_totals": {
          "description": "Totals for employee taxes withheld.",
          "total_employee_taxes": {
            "current": null,
            "ytd": null,
            "confidence": 0.0
          },
          "notes": ""
        }
      },

      "deductions": {
        "description": "Employee deductions and memos such as 401k, medical, garnishments, levies, etc.",
        "deduction_lines": [
          {
            "deduction_code": null,
            "deduction_description": null,

            "deduction_type": {
              "description": "Optional normalization bucket if it can be inferred.",
              "value": null,
              "allowed_values": [
                "Pre-Tax Deduction",
                "Post-Tax Deduction",
                "Garnishment",
                "Benefit",
                "Memo",
                "Other"
              ],
              "confidence": 0.0
            },

            "amount": {
              "current": null,
              "ytd": null,
              "confidence": 0.0
            },

            "notes": ""
          }
        ],

        "deductions_totals": {
          "description": "Totals of all deductions for the employee.",
          "total_deductions": {
            "current": null,
            "ytd": null,
            "confidence": 0.0
          },
          "notes": ""
        }
      },

      "net_pay": {
        "description": "Net pay after deductions and employee taxes.",
        "net_amount": {
          "current": null,
          "ytd": null,
          "confidence": 0.0
        },
        "notes": ""
      },

      "employee_totals": {
        "description": "Convenience rollup for the employee, used when report prints a totals row.",
        "gross_pay": {
          "current": null,
          "ytd": null,
          "confidence": 0.0
        },
        "total_employee_taxes": {
          "current": null,
          "ytd": null,
          "confidence": 0.0
        },
        "total_deductions": {
          "current": null,
          "ytd": null,
          "confidence": 0.0
        },
        "net_pay": {
          "current": null,
          "ytd": null,
          "confidence": 0.0
        },
        "notes": ""
      }
    }
  ],

  "rollups": {
    "description": "Totals beyond employee-level. Optional depending on report type.",

    "department_totals": [
      {
        "department": null,
        "totals": {
          "gross_pay": { "current": null, "ytd": null, "confidence": 0.0 },
          "total_employee_taxes": { "current": null, "ytd": null, "confidence": 0.0 },
          "total_deductions": { "current": null, "ytd": null, "confidence": 0.0 },
          "net_pay": { "current": null, "ytd": null, "confidence": 0.0 }
        },
        "notes": ""
      }
    ],

    "company_totals": {
      "description": "Company totals / grand totals across the payroll run.",
      "earnings_totals": {
        "gross_pay": { "current": null, "ytd": null, "confidence": 0.0 },
        "total_hours": { "current": null, "ytd": null, "confidence": 0.0 },
        "notes": ""
      },

      "employee_withholding_totals": {
        "description": "Total employee-paid taxes withheld (sum of employee tax lines).",
        "total_employee_taxes": { "current": null, "ytd": null, "confidence": 0.0 },
        "tax_lines": [
          {
            "tax_code": null,
            "tax_description": null,
            "tax_authority": { "value": null, "confidence": 0.0 },
            "tax_amount": { "current": null, "ytd": null, "confidence": 0.0 },
            "notes": ""
          }
        ],
        "notes": ""
      },

      "balance_employer_tax": {
        "description": "Employer-paid taxes (ER taxes) if the report includes them.",
        "tax_lines": [
          {
            "tax_code": null,
            "tax_description": null,
            "tax_authority": { "value": null, "confidence": 0.0 },
            "tax_amount": { "current": null, "ytd": null, "confidence": 0.0 },
            "notes": ""
          }
        ],
        "employer_tax_totals": {
          "total_employer_taxes": { "current": null, "ytd": null, "confidence": 0.0 },
          "notes": ""
        }
      },

      "deduction_totals": {
        "description": "Company totals for deductions.",
        "total_deductions": { "current": null, "ytd": null, "confidence": 0.0 },
        "deduction_lines": [
          {
            "deduction_code": null,
            "deduction_description": null,
            "deduction_type": { "value": null, "confidence": 0.0 },
            "amount": { "current": null, "ytd": null, "confidence": 0.0 },
            "notes": ""
          }
        ],
        "notes": ""
      },

      "grand_totals": {
        "description": "Final summary totals if the report prints them.",
        "gross_pay": { "current": null, "ytd": null, "confidence": 0.0 },
        "total_employee_taxes": { "current": null, "ytd": null, "confidence": 0.0 },
        "total_employer_taxes": { "current": null, "ytd": null, "confidence": 0.0 },
        "total_deductions": { "current": null, "ytd": null, "confidence": 0.0 },
        "net_pay": { "current": null, "ytd": null, "confidence": 0.0 },
        "notes": ""
      }
    }
  }
}
