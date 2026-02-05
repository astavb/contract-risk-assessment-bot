import streamlit as st

from utils import extract_text, detect_language
from clause_extraction import extract_clauses
from nlp_pipeline import analyze_clause
from risk_engine import detect_clause_types, assess_risk_level, contract_risk_score
from audit_logger import log_audit
from pdf_export import generate_pdf


# PAGE CONFIG

st.set_page_config(
    page_title="Contract Analysis & Risk Assessment Bot",
    layout="wide"
)


# GLOBAL STYLES (UPLOAD PAGE ONLY)

st.markdown("""
<style>
.main {
    background-color: #0e1117;
}

/* HERO SECTION */
.hero-wrapper {
    max-width: 900px;
    margin: 90px auto 40px auto;
    text-align: center;
}

.hero-title {
    font-size: 38px;
    font-weight: 700;
    color: #ffffff;
    line-height: 1.2;
}

.hero-subtitle {
    font-size: 16px;
    color: #9ca3af;
    margin-top: 14px;
}

/* FILE UPLOADER */
section[data-testid="stFileUploader"] {
    max-width: 900px;
    margin: 40px auto 10px auto;
    background: linear-gradient(135deg, #1f2933, #111827);
    border: 2px dashed #3b82f6;
    border-radius: 18px;
    padding: 26px;
}

section[data-testid="stFileUploader"] label {
    font-size: 17px;
    font-weight: 600;
    color: #ffffff;
}

section[data-testid="stFileUploader"] small {
    color: #9ca3af;
    font-size: 13px;
}

/* TRUST TEXT */
.trust-text {
    max-width: 900px;
    margin: 10px auto 30px auto;
    text-align: center;
    font-size: 12px;
    color: #6b7280;
}

/* RESULT CARDS */
.card {
    background:#161b22;
    padding:22px;
    border-radius:16px;
    margin-bottom:18px;
    border-left:6px solid #30363d;
}

.low { border-left-color:#198754; }
.medium { border-left-color:#fd7e14; }
.high { border-left-color:#dc3545; }

.badge {
    padding:4px 12px;
    border-radius:20px;
    font-weight:600;
    color:white;
}

.lowb { background:#198754; }
.medb { background:#fd7e14; }
.highb { background:#dc3545; }

.footer {
    opacity:0.6;
    font-size:12px;
    margin-top:30px;
}
</style>
""", unsafe_allow_html=True)


# CONTRACT TYPE DETECTION (NEW FEATURE)

def detect_contract_type(text: str) -> str:
    t = text.lower()

    if any(k in t for k in ["employee", "employer", "salary", "probation", "termination of employment"]):
        return "Employment Contract"

    if any(k in t for k in ["service provider", "scope of work", "sla", "deliverables", "services"]):
        return "Service Contract"

    if any(k in t for k in ["vendor", "supplier", "purchase order", "invoice", "supply of goods"]):
        return "Vendor Contract"

    if any(k in t for k in ["lease", "rent", "tenant", "landlord", "premises"]):
        return "Lease Agreement"

    if any(k in t for k in ["partnership", "profit sharing", "capital contribution", "partners"]):
        return "Partnership Deed"

    return "General Commercial Contract"


# UPLOAD LANDING PAGE

st.markdown("""
<div class="hero-wrapper">
    <div class="hero-title">
        Contract Analysis & Risk Assessment Bot
    </div>
    <div class="hero-subtitle">
        GenAI-powered legal risk assistant built for Indian SMEs.<br>
        Understand risks, obligations, and red flags before you sign.
    </div>
</div>
""", unsafe_allow_html=True)

uploaded = st.file_uploader(
    "Upload your contract (PDF, DOCX, TXT)",
    type=["pdf", "docx", "txt"]
)

st.markdown("""
<div class="trust-text">
    Files are processed locally. No data is stored or shared.
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="trust-text">
    This tool provides automated contract risk insights for informational purposes only and does not constitute legal advice.
</div>
""", unsafe_allow_html=True)


# HELPER FUNCTIONS

def explain_clause_plain(risk):
    if risk == "Low":
        return "This clause is informational and does not create legal or financial risk."
    elif risk == "Medium":
        return "This clause may affect your business and should be reviewed carefully."
    else:
        return "This clause can significantly impact your business and may require renegotiation."

def format_entities(entities):
    summary = {}
    for text, label in entities:
        if label == "ORG":
            summary.setdefault("Organizations", []).append(text)
        elif label == "DATE":
            summary.setdefault("Dates", []).append(text)
        elif label == "MONEY":
            summary.setdefault("Amounts", []).append(text)
        elif label in ["GPE", "LOC"]:
            summary.setdefault("Locations", []).append(text)
    return summary


# MAIN ANALYSIS FLOW

if uploaded:
    st.markdown("---")

    text = extract_text(uploaded)
    lang = detect_language(text)
    contract_type = detect_contract_type(text)

    st.subheader("Contract Classification")
    st.info(f"Detected Contract Type: {contract_type}")

    if lang == "hi":
        st.warning("Hindi contract detected. Normalized to English for analysis.")
    else:
        st.info(f"Detected language: {lang}")

    clauses = extract_clauses(text)
    if not clauses:
        st.error("No valid clauses detected.")
        st.stop()

    clause_risks = []

    st.subheader("Contract Overview")
    temp = [assess_risk_level(c) for c in clauses]
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Total Clauses", len(clauses))
    c2.metric("High Risk", temp.count("High"))
    c3.metric("Medium Risk", temp.count("Medium"))
    c4.metric("Low Risk", temp.count("Low"))

    st.markdown("---")
    st.subheader("Clause-by-Clause Analysis")

    results = []

    for i, clause in enumerate(clauses, start=1):
        risk = assess_risk_level(clause)
        clause_risks.append(risk)
        types = detect_clause_types(clause)
        nlp = analyze_clause(clause)
        ents = format_entities(nlp["entities"])

        cls = "high" if risk == "High" else "medium" if risk == "Medium" else "low"
        badge = "highb" if risk == "High" else "medb" if risk == "Medium" else "lowb"

        st.markdown(f"""
        <div class="card {cls}">
            <strong>Clause {i}</strong>
            <span class="badge {badge}">{risk} Risk</span>
        </div>
        """, unsafe_allow_html=True)

        st.write(clause[:900] + ("..." if len(clause) > 900 else ""))
        st.info(explain_clause_plain(risk))

        st.write("Why it matters:", ", ".join(types) if types else "General or administrative")

        if ents:
            st.write("Key information identified:")
            for k, v in ents.items():
                st.write(f"- {k}: {', '.join(v)}")

        if nlp["obligations"]:
            st.warning("This clause imposes obligations.")
        else:
            st.success("No obligations imposed.")

        st.markdown("---")

        results.append({"clause": i, "risk": risk})

    final_risk = contract_risk_score(clause_risks)
    st.subheader("Overall Contract Risk Assessment")

    if final_risk == "High Risk":
        st.error("High Risk Contract. Legal review recommended.")
    elif final_risk == "Medium Risk":
        st.warning("Medium Risk Contract. Review key clauses carefully.")
    else:
        st.success("Low Risk Contract. No major red flags detected.")

    audit_path = log_audit({
        "language": lang,
        "contract_type": contract_type,
        "overall_risk": final_risk,
        "clauses": results
    })
    st.caption(f"Audit log saved at: {audit_path}")

    summary_text = f"""
Contract Risk Summary

Contract Type: {contract_type}
Overall Risk: {final_risk}
Total Clauses Analyzed: {len(clauses)}

This report is for awareness only and does not constitute legal advice.
"""

    if st.button("Generate Risk Summary PDF"):
        pdf_path = generate_pdf(summary_text)
        with open(pdf_path, "rb") as f:
            st.download_button(
                "Download Risk Summary PDF",
                f,
                "contract_risk_summary.pdf",
                "application/pdf"
            )


# FOOTER

st.markdown("---")
st.markdown(
    "<div class='footer'>Informational use only. Not legal advice.</div>",
    unsafe_allow_html=True
)
