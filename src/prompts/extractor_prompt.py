"""Payroll extraction prompt - optimized for Haiku token limits"""

EXTRACTOR_PROMPT_TEMPLATE = """Extract payroll data AS-IS to JSON. Keep exact codes/descriptions.

Rules:
- Preserve exact labels: "0-Regular Pay" not "Regular"
- Use null for missing values
- No math, no normalization, no assumptions
- Extract ALL employees on page

{{
  "report_metadata": {{
    "report_title": null,
    "company_name": null,
    "company_number": null,
    "pay_period_start": null,
    "pay_period_end": null,
    "check_date": null,
    "payroll_number": null,
    "pay_frequency": null
  }},
  "employees": [{{
    "employee_name": null,
    "employee_id": null,
    "ssn_masked": null,
    "department": null,
    "payment_type": null,
    "check_number": null,
    "state": null,
    "tax_status_federal": null,
    "tax_allowances_federal": null,
    "earnings": [{{"raw_code": null, "raw_description": null, "rate": null, "hours_current": null, "hours_ytd": null, "amount_current": null, "amount_ytd": null}}],
    "deductions": [{{"raw_code": null, "raw_description": null, "amount_current": null, "amount_ytd": null}}],
    "taxes": [{{"raw_code": null, "raw_description": null, "amount_current": null, "amount_ytd": null}}],
    "totals": {{"gross_pay_current": null, "gross_pay_ytd": null, "total_deductions_current": null, "total_deductions_ytd": null, "total_taxes_current": null, "total_taxes_ytd": null, "net_pay_current": null, "net_pay_ytd": null}}
  }}]
}}

EXTRACTION NOTES:
- Earnings: Keep full code+description (e.g., "4-401K Plan")
- Deductions: Same as earnings
- Taxes: Preserve state prefix if present (e.g., "MA: State WH")
- Current = this period, YTD = cumulative
- Negative values: preserve formatting "(5.50)" or "-5.50"

TEXT TO EXTRACT:

{payroll_text}

OUTPUT ONLY JSON."""


def get_extractor_prompt(payroll_text: str) -> str:
    """Format extractor prompt with payroll text."""
    return EXTRACTOR_PROMPT_TEMPLATE.format(payroll_text=payroll_text)

