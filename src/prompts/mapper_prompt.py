"""Schema mapping prompt - optimized for Haiku token limits"""

MAPPER_PROMPT_TEMPLATE = """Map payroll types to normalized categories using aliases.

EARNING TYPES: Regular, Overtime, Vacation, Sick, Holiday, Bonus, Commission, Other
- "0-Regular Pay", "Regular", "REG" → Regular
- "Overtime", "OT", "1-OT" → Overtime
- "Vacation", "VAC", "PTO" → Vacation
- "Sick", "Sick Pay" → Sick

DEDUCTION TYPES: 401k, 403b, Health, Dental, Vision, FSA, HSA, Garnishment, Other
- "401K", "401(k)", "4-401K Plan" → 401k
- "Health", "CAF Medical", "Medical" → Health
- "Dental", "CAF Dental" → Dental
- "Child Support", "Tax Levy" → Garnishment

TAX TYPES: Fed, OASDI, Medicare, State, Local, SDI, SUI, Other
- "Federal WH", "FWT" → Fed
- "OASDI", "Social Security" → OASDI
- "Medicare", "Medicare WH" → Medicare
- "State WH", "SDI", "SUI" → State
- Extract jurisdiction from descriptions (e.g., "MA" from "MA: State WH")

Return JSON array with format:
[{{
  "type": "earning/deduction/tax",
  "raw_description": "original text",
  "mapped_type": "normalized category",
  "confidence": 0.95
}}, ...]

Use confidence: 1.0=exact match, 0.7-0.9=probable, <0.7=uncertain
NO inferences - only classify what exists.

DATA:
{interim_data}

OUTPUT JSON ARRAY ONLY."""


def get_mapper_prompt(interim_data: dict) -> str:
    """Format mapper prompt with interim data."""
    import json
    interim_text = json.dumps(interim_data.get('employees', []), indent=1)
    return MAPPER_PROMPT_TEMPLATE.format(interim_data=interim_text)
