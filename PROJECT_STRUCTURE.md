# Project Structure Overview

## ✅ Structure Created

```
Payroll_data_extraction/
├── main.py                          # Main orchestrator
├── requirements.txt                 # Python dependencies
├── .env.example                     # Environment variables template
├── .gitignore                       # Git ignore rules
├── README.md                        # Project documentation
├── project_plan.md                  # Original project plan
│
├── src/                            # Source code
│   ├── __init__.py
│   ├── step1_pdf_extraction.py     # Step 1: Extract text from PDF
│   ├── step2_raw_extraction.py     # Step 2: Raw extraction (PASS 1)
│   ├── step3_schema_mapping.py     # Step 3: Map to schema (PASS 2)
│   ├── step4_validation.py         # Step 4: Validate output
│   └── prompts/
│       ├── extractor_prompt.py     # PASS 1 prompt
│       └── mapper_prompt.py        # PASS 2 prompt
│
├── schemas/                        # Schema files
│   ├── global_schema.py            # ⭐ Main Python schema
│   ├── global_schema_v2.py         # Original JSON version
│   ├── SCHEMA_SUMMARY.md
│   ├── SCHEMA_MAPPING_EXAMPLE.md
│   └── SCHEMA_REVIEW.md
│
├── sample_pdfs/                    # Sample payroll PDFs
│   ├── PR-Register.pdf
│   ├── Sample-Employee-Earnings-and-Taxes-Report.pdf
│   └── Sample-Payroll-Register-Report.pdf
│
├── outputs/                        # Output folder (empty, ready for use)
│   └── (PDF folders will be created here)
│
├── testing/                        # Testing scripts and outputs
│   ├── README.md
│   ├── examine_pdfs.py
│   ├── extract_all_pdfs.py
│   └── pdf_text_*.json
│
└── Excode_vscode/                  # Reference: Old financial project
    └── (financial extraction code)
```

## Pipeline Flow

```
main.py
  │
  ├─→ Step 1: PDF Text Extraction
  │     Input:  sample_pdfs/PR-Register.pdf
  │     Output: outputs/PR-Register/extracted.json
  │
  ├─→ Step 2: Raw Extraction (PASS 1)
  │     Input:  extracted.json
  │     Prompt: prompts/extractor_prompt.py
  │     LLM:    Claude (via Anthropic API)
  │     Output: outputs/PR-Register/interim.json
  │
  ├─→ Step 3: Schema Mapping (PASS 2)
  │     Input:  interim.json + global_schema.py
  │     Prompt: prompts/mapper_prompt.py
  │     LLM:    Claude (via Anthropic API)
  │     Output: outputs/PR-Register/mapped.json
  │
  └─→ Step 4: Validation
        Input:  mapped.json
        Checks: Math validation, data types, required fields
        Output: outputs/PR-Register/final.json
```

## Output Structure (Example)

After running `python main.py PR-Register.pdf`:

```
outputs/
└── PR-Register/
    ├── extracted.json    # Raw PDF text
    ├── interim.json      # Pass 1: Raw extraction
    ├── mapped.json       # Pass 2: Mapped to schema
    └── final.json        # Validated final output
```

## Setup Required

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Configure API Key
```bash
# Copy .env.example to .env
copy .env.example .env

# Edit .env and add your Anthropic API key
ANTHROPIC_API_KEY=sk-ant-...
```

### 3. Test Structure
```bash
python main.py
```

## Implementation Status

- [x] Project structure created
- [x] Placeholder files created
- [x] Dependencies defined
- [x] Schema finalized
- [ ] Step 1: PDF Extraction - **Next**
- [ ] Step 2: Raw Extraction (PASS 1)
- [ ] Step 3: Schema Mapping (PASS 2)
- [ ] Step 4: Validation
- [ ] End-to-end testing

## Next Steps

**Ready to implement Step 1: PDF Text Extraction**

This step will:
1. Take a PDF filename as input
2. Extract text from each page using PyMuPDF
3. Save extracted text to JSON
4. Create output folder structure

Let me know when you're ready to proceed!
