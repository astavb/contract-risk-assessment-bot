import streamlit as st

from utils import extract_text, detect_language
from clause_extraction import extract_clauses
from nlp_pipeline import analyze_clause
from risk_engine import (
    detect_clause_types,
    assess_risk_level,
    contract_risk_score
)
from pdf_export import generate_pdf
from audit_logger import log_audit

# -------------------------------------------------
# PAGE CONFIG
# -------------------------------------------------
st.set_page_config(
    page_title="Contract Analysis & Risk Assessment Bot",
    layout="wide"
)

# -------------------------------------------------
# HEADER
# -------------------------------------------------
st.markdown(
    "<h1 style='text-align:center;'>Contract Analysis & Risk Assessment Bot</h1>",
    unsafe_allow_html=True
)
st.markdown(
    "<p style='text-align:center;color:gray;'>GenAI-powered legal risk assistant for Indian SMEs</p>",
    unsafe_allow_html=True
)
st.markdown("---")

# -------------------------------------------------
# UPLOAD SECTION
# -------------------------------------------------
uploaded_file = st.file_uploader(
    "Upload your contract (PDF, DOCX, TXT)",
    type=["pdf", "docx", "txt"]
)

st.caption("Files are processed locally. No data is shared.")
st.warning("This tool provides automated contract risk insights for informational purposes only.")

# -------------------------------------------------
# MAIN LOGIC
# -------------------------------------------------
if uploaded_file:
    with st.spinner("Reading contract..."):
        text = extract_text(uploaded_file)
        language = detect_language(text)

    st.info(f"Detected language: {language}")

    clauses = extract_clauses(text)

    if not clauses:
        st.error("No clauses detected in the uploaded document.")
        st.stop()

    clause_results = []
    risk_levels = []

    # -------------------------------------------------
    # CLAUSE ANALYSIS
    # -------------------------------------------------
    for idx, clause in enumerate(clauses, start=1):
        nlp_result = analyze_clause(clause)
        clause_types = detect_clause_types(clause)
        risk_level = assess_risk_level(clause)

        risk_levels.append(risk_level)

        clause_results.append({
            "index": idx,
            "text": clause,
            "risk": risk_level,
            "clause_types": clause_types,
            "entities": nlp_result.get("entities", []),
            "has_obligation": nlp_result.get("has_obligation", False),
            "has_prohibition": nlp_result.get("has_prohibition", False),
            "has_right": nlp_result.get("has_right", False)
        })

    # -------------------------------------------------
    # OVERVIEW
    # -------------------------------------------------
    st.markdown("## Contract Overview")

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Clauses", len(clauses))
    col2.metric("High Risk", risk_levels.count("High"))
    col3.metric("Medium Risk", risk_levels.count("Medium"))
    col4.metric("Low Risk", risk_levels.count("Low"))

    st.markdown("---")

    # -------------------------------------------------
    # CLAUSE-BY-CLAUSE DISPLAY
    # -------------------------------------------------
    st.markdown("## Clause-by-Clause Analysis")

    for result in clause_results:
        with st.expander(f"Clause {result['index']} | {result['risk']} Risk"):
            st.markdown("**Clause Text**")
            st.write(result["text"])

            # Risk explanation
            if result["risk"] == "High":
                st.error("This clause poses a significant legal or financial risk for SMEs.")
            elif result["risk"] == "Medium":
                st.warning("This clause may require review depending on business context.")
            else:
                st.success("This clause is informational and low risk.")

            # Clause types
            st.markdown("**Detected Clause Types**")
            if result["clause_types"]:
                for ct in result["clause_types"]:
                    st.write(f"- {ct}")
            else:
                st.write("General")

            # Legal signals
            st.markdown("**Legal Signals**")
            signals = []
            if result["has_obligation"]:
                signals.append("Obligation")
            if result["has_prohibition"]:
                signals.append("Prohibition")
            if result["has_right"]:
                signals.append("Right")

            st.write(", ".join(signals) if signals else "None")

            # Named entities
            if result["entities"]:
                st.markdown("**Named Entities**")
                for ent, label in result["entities"]:
                    st.write(f"- {ent} ({label})")

    # -------------------------------------------------
    # OVERALL RISK
    # -------------------------------------------------
    st.markdown("---")
    st.markdown("## Overall Contract Risk Assessment")

    overall_risk = contract_risk_score(risk_levels)

    if overall_risk == "High Risk":
        st.error("High Risk Contract – legal review strongly recommended.")
    elif overall_risk == "Medium Risk":
        st.warning("Medium Risk Contract – review key clauses carefully.")
    else:
        st.success("Low Risk Contract – no major legal concerns detected.")

    # -------------------------------------------------
    # AUDIT LOG
    # -------------------------------------------------
    audit_path = log_audit({
        "language": language,
        "total_clauses": len(clauses),
        "risk_levels": risk_levels,
        "overall_risk": overall_risk
    })
    st.caption(f"Audit log saved at: {audit_path}")

    # -------------------------------------------------
    # PDF EXPORT
    # -------------------------------------------------
    if st.button("Export Risk Summary as PDF"):
        pdf_path = generate_pdf(
            overall_risk=overall_risk,
            total_clauses=len(clauses)
        )

        with open(pdf_path, "rb") as f:
            st.download_button(
                "Download PDF",
                f,
                file_name="contract_risk_summary.pdf",
                mime="application/pdf"
            )

