# Setup Instructions

## Quick Setup

### 1. Verify Python Environment
```bash
# Check Python version (should be 3.8+)
python --version
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure API Key
```bash
# Copy the example file
copy .env.example .env

# Edit .env and add your Anthropic API key
# Get your key from: https://console.anthropic.com/
```

Your `.env` file should look like:
```
ANTHROPIC_API_KEY=sk-ant-api03-...your-actual-key...
```

### 4. Test the Setup
```bash
python main.py
```

You should see:
```
============================================================
PAYROLL DATA EXTRACTION PIPELINE
============================================================
Started: 2026-01-05 20:17:27

Pipeline structure created!
Ready for implementation...
```

## Troubleshooting

### Missing Dependencies
```bash
pip install pymupdf anthropic python-dotenv
```

### API Key Not Found
Make sure:
1. `.env` file exists in the project root
2. File contains `ANTHROPIC_API_KEY=your_key`
3. No quotes around the key value

### Import Errors
Make sure you're running from the project root directory:
```bash
cd "C:\Users\Akshit\Desktop\Document Retrieval\Payroll_data_extraction"
python main.py
```

## Verification Checklist

- [ ] Python 3.8+ installed
- [ ] Virtual environment activated (`.venv/`)
- [ ] Dependencies installed (`pymupdf`, `anthropic`, `python-dotenv`)
- [ ] `.env` file created with valid API key
- [ ] `main.py` runs without errors
- [ ] Project structure matches `PROJECT_STRUCTURE.md`

## Ready for Implementation!

Once setup is complete, you're ready to implement the pipeline steps.
