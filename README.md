# Contract Analysis & Risk Assessment Bot

A GenAI-powered legal assistant designed to help Indian SMEs understand complex contracts, identify legal risks, and receive actionable insights in plain business language.

##  Features

- Contract type classification (Employment, Service, Vendor, Lease, Partnership)
- Clause-by-clause analysis with risk scoring
- Plain-English explanations for non-legal users
- Detection of unfavorable clauses (indemnity, termination, non-compete, jurisdiction, etc.)
- English and Hindi contract support
- Overall contract risk assessment
- Downloadable PDF risk summary
- Local audit logging for confidentiality

##  Tech Stack

- Python
- Streamlit
- spaCy (NLP preprocessing)
- GPT-4 (legal reasoning)
- ReportLab (PDF export)

##  Supported File Formats

- PDF (text-based)
- DOC/DOCX
- TXT

##  Privacy

All files are processed locally. No data is stored or shared externally.

##  How to Run Locally

```bash
pip install -r requirements.txt
streamlit run app.py
