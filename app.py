import streamlit as st
from utils import extract_text, detect_language
from clause_extraction import split_into_clauses
from nlp_pipeline import analyze_clause
from risk_engine import assess_risk_level, detect_clause_types, contract_risk_score
from audit_logger import save_audit_log
from pdf_export import generate_pdf
import os

# -----------------------------
# Page config
# -----------------------------
st.set_page_config(
    page_title="Contract Analysis & Risk Assessment Bot",
    layout="wide"
)

# -----------------------------
# Header
# -----------------------------
st.title("Contract Analysis & Risk Assessment Bot")
st.caption("GenAI-powered legal risk assistant built for Indian SMEs")

st.markdown("---")

# -----------------------------
# Upload section (UNCHANGED UI)
# -----------------------------
uploaded_file = st.file_uploader(
    "Upload your contract (PDF, DOCX, TXT)",
    type=["pdf", "docx", "txt"]
)

st.caption("Files are processed locally. No data is shared.")
st.warning("This tool provides automated contract risk insights for informational purposes only and does not constitute legal advice.")

# -----------------------------
# Main logic
# -----------------------------
if uploaded_file:
    # Extract text
    contract_text = extract_text(uploaded_file)

    if not contract_text.strip():
        st.error("Unable to extract text from this document.")
        st.stop()

    # Language detection
    language = detect_language(contract_text)

    # Contract type classification (simple heuristic)
    contract_type = "General Contract"
    text_lower = contract_text.lower()

    if "employment" in text_lower or "employee" in text_lower:
        contract_type = "Employment Contract"
    elif "service" in text_lower:
        contract_type = "Service Contract"
    elif "vendor" in text_lower or "supplier" in text_lower:
        contract_type = "Vendor Contract"
    elif "lease" in text_lower or "rent" in text_lower:
        contract_type = "Lease Agreement"
    elif "partnership" in text_lower:
        contract_type = "Partnership Deed"

    # -----------------------------
    # Contract classification UI
    # -----------------------------
    st.subheader("Contract Classification")

    st.info(f"Detected Contract Type: {contract_type}")
    st.info(f"Detected Language: {language}")

    # -----------------------------
    # Clause extraction
    # -----------------------------
    clauses = split_into_clauses(contract_text)

    clause_results = []
    risk_levels = []

    for idx, clause in enumerate(clauses, start=1):
        nlp_result = analyze_clause(clause)
        risk_level = assess_risk_level(clause)
        clause_types = detect_clause_types(clause)

        clause_data = {
            "index": idx,
            "text": clause,
            "risk": risk_level,
            "types": clause_types,
            "explanation": nlp_result.get("plain_explanation", ""),
            "why_it_matters": nlp_result.get("why_it_matters", "General or administrative")
        }

        clause_results.append(clause_data)
        risk_levels.append(risk_level)

    # -----------------------------
    # Overview metrics
    # -----------------------------
    overall_risk = contract_risk_score(risk_levels)

    high_count = risk_levels.count("High")
    medium_count = risk_levels.count("Medium")
    low_count = risk_levels.count("Low")

    st.markdown("---")
    st.subheader("Contract Overview")

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Clauses", len(clauses))
    col2.metric("High Risk", high_count)
    col3.metric("Medium Risk", medium_count)
    col4.metric("Low Risk", low_count)

    # -----------------------------
    # Clause-by-clause UI (OLD STYLE)
    # -----------------------------
    st.markdown("---")
    st.subheader("Clause-by-Clause Analysis")

    for c in clause_results:
        risk_color = "🟢 Low Risk"
        if c["risk"] == "High":
            risk_color = "🔴 High Risk"
        elif c["risk"] == "Medium":
            risk_color = "🟡 Medium Risk"

        with st.expander(f"Clause {c['index']} | {risk_color}", expanded=(c["index"] == 1)):
            st.markdown(c["text"])

            if c["explanation"]:
                st.success(c["explanation"])
            else:
                st.info("This clause is informational and does not create legal or financial risk.")

            st.markdown(f"**Why it matters:** {c['why_it_matters']}")

            if c["types"]:
                st.markdown("**Detected Clause Types:**")
                for t in c["types"]:
                    st.write(f"- {t}")

    # -----------------------------
    # Overall risk section
    # -----------------------------
    st.markdown("---")
    st.subheader("Overall Contract Risk Assessment")

    if overall_risk == "High Risk":
        st.error("High Risk Contract – immediate legal review recommended.")
    elif overall_risk == "Medium Risk":
        st.warning("Medium Risk Contract – review key clauses carefully.")
    else:
        st.success("Low Risk Contract – no major red flags detected.")

    # -----------------------------
    # Audit log
    # -----------------------------
    audit_path = save_audit_log(
        contract_type=contract_type,
        language=language,
        overall_risk=overall_risk,
        clauses=clause_results
    )

    st.caption(f"Audit log saved at: {audit_path}")

    # -----------------------------
    # PDF export (FIXED)
    # -----------------------------
    st.markdown("---")
    if st.button("Export Risk Summary as PDF"):
        output_path = "outputs/contract_risk_summary.pdf"

        pdf_path = generate_pdf(
            output_path=output_path,
            contract_type=contract_type,
            overall_risk=overall_risk,
            total_clauses=len(clause_results),
            clause_summary=clause_results
        )

        with open(pdf_path, "rb") as f:
            st.download_button(
                label="Download PDF",
                data=f,
                file_name="contract_risk_summary.pdf",
                mime="application/pdf"
            )




