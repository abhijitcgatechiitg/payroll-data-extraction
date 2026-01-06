"""
Global Payroll Schema (Python Dictionary Format)
This schema represents a universal structure for payroll data extraction.
It supports multiple employees, various earning types, deductions, taxes, and rollups.
"""

GLOBAL_PAYROLL_SCHEMA = {
    "section": "PayrollRegister",
    
    "metadata": {
        "description": "Report-level metadata and document information",
        
        "source_filename": None,
        "extraction_timestamp": None,
        
        "currency": {
            "description": "Currency used in the report (e.g., USD, CAD, EUR)",
            "code": None,  # ISO code like "USD"
            "symbol": None,  # Symbol like "$"
            "confidence": 0.0
        },
        
        "report_metadata": {
            "description": "High-level report header information",
            
            "report_title": None,  # e.g., "PAYROLL REGISTER"
            
            "report_type": {
                "description": "Normalized classification of payroll report type",
                "value": None,
                "allowed_values": [
                    "Payroll Register",
                    "Employee Earnings and Taxes",
                    "Payroll Summary",
                    "Pay Stub",
                    "Wage Statement",
                    "Other"
                ],
                "confidence": 0.0
            },
            
            "employer_info": {
                "description": "Employer/company information from report header",
                "company_name": None,
                "company_id": None,
                "company_number": None,  # Some reports have Co. No.
                "address": None,
                "worksite_or_location": None,
                "notes": ""
            },
            
            "report_period": {
                "description": "Pay period and check date information",
                
                "pay_frequency": {
                    "description": "How often employees are paid",
                    "value": None,
                    "allowed_values": [
                        "Weekly",
                        "Biweekly",
                        "Semi-Monthly",
                        "Monthly",
                        "Quarterly",
                        "Other"
                    ],
                    "confidence": 0.0
                },
                
                "period_start_date": None,  # Pay period start
                "period_end_date": None,    # Pay period end
                "check_date": None,         # Date checks are issued
                "notes": ""
            },
            
            "run_info": {
                "description": "Payroll run information",
                "payroll_number": None,  # Payroll run number
                "batch_id": None,
                "generated_datetime": None,
                "generated_by": None,
                "system_name": None
            },
            
            "document_refs": {
                "description": "Document page and reference information",
                "page_number": None,
                "total_pages": None,
                "notes": ""
            }
        }
    },
    
    "employees": [
        {
            "employee_info": {
                "description": "Employee identification and classification",
                
                "employee_name": None,
                "employee_id": None,        # Employee number
                "ssn_masked": None,         # Masked SSN (e.g., *******6132)
                
                "department": None,         # Department or Dept. No.
                "location": None,
                "state": None,              # State for tax purposes
                
                "employment_type": {
                    "description": "Employment classification if detectable",
                    "value": None,
                    "allowed_values": [
                        "Full-Time",
                        "Part-Time",
                        "Contractor",
                        "Temporary",
                        "Seasonal",
                        "Other"
                    ],
                    "confidence": 0.0
                },
                
                "pay_type": {
                    "description": "Hourly vs Salaried classification if detectable",
                    "value": None,
                    "allowed_values": ["Hourly", "Salaried", "Other"],
                    "confidence": 0.0
                },
                
                "pay_frequency": None,      # Weekly, Biweekly, etc.
                "job_title": None,
                
                "tax_profile": {
                    "description": "Tax filing status and withholding setup",
                    
                    "federal_filing_status": None,  # Single, Married
                    "federal_allowances": None,     # Number of allowances/dependents
                    
                    "state_filing_status": None,
                    "state_allowances": None,
                    
                    "additional_withholding": None,
                    "notes": ""
                },
                
                "notes": ""
            },
            
            "payment_info": {
                "description": "Payment method and details for this payroll run",
                
                "payment_type": {
                    "description": "How employee receives payment",
                    "value": None,
                    "allowed_values": [
                        "Check",
                        "Direct Deposit",
                        "DD",  # Abbreviation for Direct Deposit
                        "Cash",
                        "Other"
                    ],
                    "confidence": 0.0
                },
                
                "check_number": None,       # Check or voucher number
                "bank_account_masked": None,
                "pay_date": None,
                "notes": ""
            },
            
            "earnings": {
                "description": "All earning types for this employee",
                
                "earning_lines": [
                    {
                        "description": "Individual earning line item (e.g., Regular, Overtime, Bonus)",
                        
                        "earning_code": None,         # e.g., "0", "1", "REG", "OT"
                        "earning_description": None,  # e.g., "Regular Pay", "Vacation Pay"
                        
                        "earning_type": {
                            "description": "Normalized earning category",
                            "value": None,
                            "allowed_values": [
                                "Regular Pay",
                                "Overtime",
                                "Double Time",
                                "Vacation Pay",
                                "Sick Pay",
                                "Holiday Pay",
                                "Bonus",
                                "Commission",
                                "Severance",
                                "Retroactive Pay",
                                "Other"
                            ],
                            "confidence": 0.0
                        },
                        
                        "rate": {
                            "description": "Hourly rate or pay rate",
                            "value": None,
                            "confidence": 0.0
                        },
                        
                        "hours": {
                            "description": "Hours worked for this earning type",
                            "current": None,
                            "ytd": None,
                            "confidence": 0.0
                        },
                        
                        "amount": {
                            "description": "Amount paid for this earning line",
                            "current": None,
                            "ytd": None,
                            "confidence": 0.0
                        },
                        
                        "taxable_flags": {
                            "description": "Tax applicability flags if shown",
                            "federal_taxable": None,
                            "fica_taxable": None,
                            "state_taxable": None,
                            "sui_taxable": None  # State Unemployment Insurance
                        },
                        
                        "notes": ""
                    }
                ],
                
                "earnings_totals": {
                    "description": "Summary totals for all earnings",
                    
                    "gross_pay": {
                        "description": "Total gross earnings before any deductions",
                        "current": None,
                        "ytd": None,
                        "confidence": 0.0
                    },
                    
                    "total_hours": {
                        "description": "Total hours worked",
                        "current": None,
                        "ytd": None,
                        "confidence": 0.0
                    },
                    
                    "notes": ""
                }
            },
            
            "employee_taxes": {
                "description": "Employee-paid taxes (withholdings)",
                
                "tax_lines": [
                    {
                        "description": "Individual tax withholding line",
                        
                        "tax_code": None,         # e.g., "FWT", "FICA", "SWT"
                        "tax_description": None,  # e.g., "Federal WH", "OASDI", "Medicare"
                        
                        "tax_type": {
                            "description": "Normalized tax category",
                            "value": None,
                            "allowed_values": [
                                "Federal Income Tax",
                                "Federal WH",
                                "OASDI",           # Social Security
                                "Medicare",
                                "State Income Tax",
                                "State WH",
                                "Local Income Tax",
                                "SDI",             # State Disability Insurance
                                "SUI",             # State Unemployment Insurance
                                "Other"
                            ],
                            "confidence": 0.0
                        },
                        
                        "tax_authority": {
                            "description": "Federal, State, or Local",
                            "value": None,
                            "allowed_values": ["Federal", "State", "Local", "Other"],
                            "confidence": 0.0
                        },
                        
                        "jurisdiction": None,  # e.g., "MA", "CA", "NYC" for state/local taxes
                        
                        "tax_amount": {
                            "description": "Amount withheld",
                            "current": None,
                            "ytd": None,
                            "confidence": 0.0
                        },
                        
                        "notes": ""
                    }
                ],
                
                "employee_tax_totals": {
                    "description": "Total employee taxes withheld",
                    
                    "total_employee_taxes": {
                        "current": None,
                        "ytd": None,
                        "confidence": 0.0
                    },
                    
                    "notes": ""
                }
            },
            
            "deductions": {
                "description": "Employee deductions (401k, insurance, garnishments, etc.)",
                
                "deduction_lines": [
                    {
                        "description": "Individual deduction line item",
                        
                        "deduction_code": None,         # e.g., "4", "401K", "MED"
                        "deduction_description": None,  # e.g., "401K Plan", "CAF Medical"
                        
                        "deduction_type": {
                            "description": "Category of deduction",
                            "value": None,
                            "allowed_values": [
                                "Retirement - 401k",
                                "Retirement - 403b",
                                "Retirement - IRA",
                                "Retirement - Other",
                                "Health Insurance",
                                "Dental Insurance",
                                "Vision Insurance",
                                "Life Insurance",
                                "Disability Insurance",
                                "FSA",              # Flexible Spending Account
                                "HSA",              # Health Savings Account
                                "Garnishment",
                                "Child Support",
                                "Tax Levy",
                                "Union Dues",
                                "Loan Repayment",
                                "Other Pre-Tax",
                                "Other Post-Tax",
                                "Memo Only",        # Informational, not actual deduction
                                "Other"
                            ],
                            "confidence": 0.0
                        },
                        
                        "is_pre_tax": {
                            "description": "Whether deduction is taken before tax calculation",
                            "value": None,
                            "confidence": 0.0
                        },
                        
                        "amount": {
                            "description": "Amount deducted",
                            "current": None,
                            "ytd": None,
                            "confidence": 0.0
                        },
                        
                        "notes": ""
                    }
                ],
                
                "deductions_totals": {
                    "description": "Total deductions for employee",
                    
                    "total_deductions": {
                        "current": None,
                        "ytd": None,
                        "confidence": 0.0
                    },
                    
                    "notes": ""
                }
            },
            
            "net_pay": {
                "description": "Final net pay after all deductions and taxes",
                
                "net_amount": {
                    "description": "Net pay = Gross - Taxes - Deductions",
                    "current": None,
                    "ytd": None,
                    "confidence": 0.0
                },
                
                "notes": ""
            },
            
            "employee_totals": {
                "description": "Summary row for employee if report shows one",
                
                "gross_pay": {
                    "current": None,
                    "ytd": None,
                    "confidence": 0.0
                },
                
                "total_employee_taxes": {
                    "current": None,
                    "ytd": None,
                    "confidence": 0.0
                },
                
                "total_deductions": {
                    "current": None,
                    "ytd": None,
                    "confidence": 0.0
                },
                
                "net_pay": {
                    "current": None,
                    "ytd": None,
                    "confidence": 0.0
                },
                
                "notes": ""
            }
        }
    ],
    
    "rollups": {
        "description": "Company-level and department-level totals",
        
        "department_totals": [
            {
                "department": None,
                "department_number": None,
                
                "totals": {
                    "gross_pay": {
                        "current": None,
                        "ytd": None,
                        "confidence": 0.0
                    },
                    
                    "total_employee_taxes": {
                        "current": None,
                        "ytd": None,
                        "confidence": 0.0
                    },
                    
                    "total_deductions": {
                        "current": None,
                        "ytd": None,
                        "confidence": 0.0
                    },
                    
                    "net_pay": {
                        "current": None,
                        "ytd": None,
                        "confidence": 0.0
                    }
                },
                
                "notes": ""
            }
        ],
        
        "company_totals": {
            "description": "Grand totals across entire payroll run",
            
            "earnings_totals": {
                "description": "Company-wide earnings summary",
                
                "gross_pay": {
                    "current": None,
                    "ytd": None,
                    "confidence": 0.0
                },
                
                "total_hours": {
                    "current": None,
                    "ytd": None,
                    "confidence": 0.0
                },
                
                "earning_breakdown": [
                    {
                        "description": "Breakdown by earning type if available",
                        "earning_type": None,
                        "current": None,
                        "ytd": None,
                        "confidence": 0.0
                    }
                ],
                
                "notes": ""
            },
            
            "employee_withholding_totals": {
                "description": "Total employee-paid taxes across company",
                
                "total_employee_taxes": {
                    "current": None,
                    "ytd": None,
                    "confidence": 0.0
                },
                
                "tax_lines": [
                    {
                        "description": "Breakdown by tax type",
                        "tax_code": None,
                        "tax_description": None,
                        "tax_authority": {
                            "value": None,
                            "confidence": 0.0
                        },
                        "tax_amount": {
                            "current": None,
                            "ytd": None,
                            "confidence": 0.0
                        },
                        "notes": ""
                    }
                ],
                
                "notes": ""
            },
            
            "employer_taxes": {
                "description": "Employer-paid taxes (if report includes them)",
                
                "tax_lines": [
                    {
                        "description": "Employer share of taxes",
                        "tax_code": None,
                        "tax_description": None,  # e.g., "ER FICA", "ER Medicare", "FUTA", "SUTA"
                        
                        "tax_type": {
                            "value": None,
                            "allowed_values": [
                                "Employer FICA",
                                "Employer Medicare",
                                "FUTA",  # Federal Unemployment Tax
                                "SUTA",  # State Unemployment Tax
                                "Workers Comp",
                                "Other"
                            ],
                            "confidence": 0.0
                        },
                        
                        "tax_authority": {
                            "value": None,
                            "confidence": 0.0
                        },
                        
                        "tax_amount": {
                            "current": None,
                            "ytd": None,
                            "confidence": 0.0
                        },
                        
                        "notes": ""
                    }
                ],
                
                "employer_tax_totals": {
                    "total_employer_taxes": {
                        "current": None,
                        "ytd": None,
                        "confidence": 0.0
                    },
                    "notes": ""
                }
            },
            
            "deduction_totals": {
                "description": "Company-wide deduction totals",
                
                "total_deductions": {
                    "current": None,
                    "ytd": None,
                    "confidence": 0.0
                },
                
                "deduction_lines": [
                    {
                        "description": "Breakdown by deduction type",
                        "deduction_code": None,
                        "deduction_description": None,
                        "deduction_type": {
                            "value": None,
                            "confidence": 0.0
                        },
                        "amount": {
                            "current": None,
                            "ytd": None,
                            "confidence": 0.0
                        },
                        "notes": ""
                    }
                ],
                
                "notes": ""
            },
            
            "grand_totals": {
                "description": "Final summary for entire payroll",
                
                "employee_count": None,
                
                "gross_pay": {
                    "current": None,
                    "ytd": None,
                    "confidence": 0.0
                },
                
                "total_hours": {
                    "current": None,
                    "ytd": None,
                    "confidence": 0.0
                },
                
                "total_employee_taxes": {
                    "current": None,
                    "ytd": None,
                    "confidence": 0.0
                },
                
                "total_employer_taxes": {
                    "current": None,
                    "ytd": None,
                    "confidence": 0.0
                },
                
                "total_deductions": {
                    "current": None,
                    "ytd": None,
                    "confidence": 0.0
                },
                
                "net_pay": {
                    "current": None,
                    "ytd": None,
                    "confidence": 0.0
                },
                
                "notes": ""
            }
        }
    }
}


# Aliases for mapping (used during Pass 2)
FIELD_ALIASES = {
    # Earning types
    "earnings": {
        "Regular Pay": ["Regular", "Reg Pay", "Regular Pay", "0-Regular Pay", "REG", "Regular Hours"],
        "Overtime": ["Overtime", "OT", "O/T", "Overtime Pay", "1-Overtime", "OT Pay"],
        "Double Time": ["Double Time", "DT", "Double OT", "2-Double Time"],
        "Vacation Pay": ["Vacation", "Vacation Pay", "1-Vacation Pay", "VAC", "PTO"],
        "Sick Pay": ["Sick", "Sick Pay", "2-Sick Pay", "Sick Leave", "Sick Time"],
        "Holiday Pay": ["Holiday", "Holiday Pay", "HOL", "Holiday Hours"],
        "Bonus": ["Bonus", "3-Bonus Pay", "Bonus Pay", "Incentive", "Annual Bonus"],
        "Commission": ["Commission", "COMM", "Sales Commission"],
    },
    
    # Tax types
    "taxes": {
        "Federal Income Tax": ["Federal WH", "FWT", "Fed WH", "Federal Withholding", "Federal Tax"],
        "OASDI": ["OASDI", "Social Security", "SS", "FICA-OASDI", "Soc Sec"],
        "Medicare": ["Medicare", "Med", "FICA-Medicare", "FICA Med"],
        "State Income Tax": ["State WH", "SWT", "State Withholding", "State Tax", "MA: State WH", "CA: State WH"],
        "Local Income Tax": ["Local WH", "City Tax", "Local Tax", "Municipal Tax"],
        "SDI": ["SDI", "State Disability", "CA SDI", "Disability Insurance"],
    },
    
    # Deduction types
    "deductions": {
        "Retirement - 401k": ["401K Plan", "4-401K Plan", "401(k)", "401k", "401K Deduction"],
        "Retirement - 403b": ["403B Plan", "403(b)", "403b"],
        "Health Insurance": ["CAF Medical", "2-CAF Medical", "Medical", "Health Ins", "Medical Insurance"],
        "Dental Insurance": ["CAF Dental", "3-CAF Dental", "Dental", "Dental Ins"],
        "Vision Insurance": ["Vision", "Vision Ins", "Vision Insurance"],
        "Life Insurance": ["Life", "Life Ins", "Life Insurance"],
        "Child Support": ["Child Support", "1-Child Support", "31-Child Support", "Garnishment-Child Support"],
        "Tax Levy": ["Tax Levy", "32-Mass Tax Lev", "IRS Levy", "State Levy"],
        "FSA": ["FSA", "Flex Spending", "Flexible Spending"],
        "HSA": ["HSA", "Health Savings"],
        "Union Dues": ["Union", "Union Dues", "Union Fee"],
    },
    
    # Payment types
    "payment_types": {
        "Direct Deposit": ["DD", "Direct Deposit", "ACH", "EFT"],
        "Check": ["Check", "CHK", "Paper Check"],
    },
    
    # Pay frequencies
    "pay_frequencies": {
        "Weekly": ["Weekly", "WK", "W"],
        "Biweekly": ["Biweekly", "Bi-Weekly", "Every 2 Weeks", "BW"],
        "Semi-Monthly": ["Semi-Monthly", "Semi Monthly", "Twice Monthly", "SM"],
        "Monthly": ["Monthly", "MO", "M"],
    }
}
