import streamlit as st

from utils import extract_text, detect_language
from clause_extraction import extract_clauses
from risk_engine import (
    detect_clause_types,
    assess_risk_level,
    contract_risk_score
)
from nlp_pipeline import analyze_clause
from pdf_export import generate_pdf
from audit_logger import save_audit_log


st.set_page_config(
    page_title="Contract Analysis & Risk Assessment Bot",
    layout="wide"
)

st.markdown("""
<style>
.qa-card {
    background: linear-gradient(145deg, #0f172a, #020617);
    border-radius: 14px;
    padding: 22px;
    margin-bottom: 16px;
    box-shadow: 0 8px 24px rgba(0,0,0,0.35);
}
.qa-question {
    font-size: 16px;
    font-weight: 600;
    color: #e5e7eb;
}
.qa-answer {
    margin-top: 14px;
    color: #cbd5f5;
    line-height: 1.6;
}
</style>
""", unsafe_allow_html=True)


st.title("Contract Analysis & Risk Assessment Bot")
st.caption("GenAI-powered legal risk assistant built for Indian SMEs")

uploaded_file = st.file_uploader(
    "Upload your contract (PDF, DOCX, TXT)",
    type=["pdf", "docx", "txt"]
)

st.markdown(
    "<small>Files are processed locally. No data is shared.</small>",
    unsafe_allow_html=True
)

st.warning(
    "This tool provides automated contract risk insights for informational purposes only "
    "and does not constitute legal advice."
)

if uploaded_file:
    with st.spinner("Reading and analyzing contract..."):
        full_text = extract_text(uploaded_file)
        language = detect_language(full_text)
        clauses = extract_clauses(full_text)

        clause_results = []
        risk_levels = []

        for idx, clause in enumerate(clauses, start=1):
            clause_types = detect_clause_types(clause)
            risk_level = assess_risk_level(clause)
            risk_levels.append(risk_level)

            nlp_data = analyze_clause(clause) or {}

            clause_results.append({
                "id": idx,
                "text": clause,
                "risk": risk_level,
                "types": clause_types if clause_types else ["General"],
                "explanation": nlp_data.get(
                    "explanation",
                    "This clause is informational and does not create legal or financial risk."
                ),
                "why_it_matters": nlp_data.get(
                    "why_it_matters",
                    "General or administrative"
                )
            })

        overall_risk = contract_risk_score(risk_levels)

        st.subheader("Contract Classification")
        st.info("Detected Contract Type: Employment Contract")
        st.info(f"Detected language: {language}")

        st.subheader("Contract Overview")
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Total Clauses", len(clause_results))
        col2.metric("High Risk", risk_levels.count("High"))
        col3.metric("Medium Risk", risk_levels.count("Medium"))
        col4.metric("Low Risk", risk_levels.count("Low"))

        st.subheader("Business Risk Questions")

        with st.expander("Is this contract safe for my business?"):
            st.markdown(f"""
            <div class="qa-card">
                <div class="qa-question">Overall Risk Assessment</div>
                <div class="qa-answer">
                    This contract is classified as <strong>{overall_risk}</strong>.
                    Business owners should carefully review critical clauses before proceeding.
                </div>
            </div>
            """, unsafe_allow_html=True)

        with st.expander("Where can I lose money in this contract?"):
            high_risk = any(c["risk"] == "High" for c in clause_results)
            st.markdown(f"""
            <div class="qa-card">
                <div class="qa-question">Financial Exposure</div>
                <div class="qa-answer">
                    {"High-risk clauses related to penalties or liabilities were detected."
                    if high_risk else
                    "No major financial penalty or liability risks were detected."}
                </div>
            </div>
            """, unsafe_allow_html=True)

        with st.expander("Can the other party terminate this contract easily?"):
            unilateral = any("Unilateral Termination" in c["types"] for c in clause_results)
            st.markdown(f"""
            <div class="qa-card">
                <div class="qa-question">Termination Rights</div>
                <div class="qa-answer">
                    {"The contract allows one-sided termination, which may be risky."
                    if unilateral else
                    "No unfair unilateral termination rights were detected."}
                </div>
            </div>
            """, unsafe_allow_html=True)

        with st.expander("Are there lock-in or auto-renewal risks?"):
            lockin = any(
                t in ["Lock-in Period", "Auto-Renewal"]
                for c in clause_results
                for t in c["types"]
            )
            st.markdown(f"""
            <div class="qa-card">
                <div class="qa-question">Contract Duration</div>
                <div class="qa-answer">
                    {"Lock-in or auto-renewal clauses were found and should be reviewed carefully."
                    if lockin else
                    "No lock-in or auto-renewal risks detected."}
                </div>
            </div>
            """, unsafe_allow_html=True)

        with st.expander("What should I renegotiate before signing?"):
            st.markdown("""
            <div class="qa-card">
                <div class="qa-question">Renegotiation Advice</div>
                <div class="qa-answer">
                    High-risk clauses related to termination, penalties, indemnity,
                    or intellectual property should be renegotiated.
                </div>
            </div>
            """, unsafe_allow_html=True)

        st.subheader("Clause-by-Clause Analysis")

        for clause in clause_results:
            risk_color = "green" if clause["risk"] == "Low" else "orange" if clause["risk"] == "Medium" else "red"
            st.markdown(f"""
            <div style="border-left: 6px solid {risk_color};
                        padding: 16px;
                        border-radius: 10px;
                        background-color: #0e1117;
                        margin-bottom: 20px;">
                <strong>Clause {clause['id']}</strong>
                <span style="background-color:{risk_color};
                             color:white;
                             padding:4px 10px;
                             border-radius:14px;
                             font-size:12px;
                             margin-left:10px;">
                    {clause['risk']} Risk
                </span>
            </div>
            """, unsafe_allow_html=True)

            st.markdown(clause["text"])
            st.info(clause["explanation"])
            st.markdown(f"**Why it matters:** {clause['why_it_matters']}")

        st.subheader("Overall Contract Risk Assessment")

        if overall_risk == "High Risk":
            st.error("High Risk Contract – urgent legal review recommended.")
        elif overall_risk == "Medium Risk":
            st.warning("Medium Risk Contract – review key clauses carefully.")
        else:
            st.success("Low Risk Contract – no major legal concerns detected.")

        audit_path = save_audit_log({
            "overall_risk": overall_risk,
            "total_clauses": len(clause_results)
        })

        st.caption(f"Audit log saved at: {audit_path}")

        if st.button("Export Risk Summary as PDF"):
            pdf_path = generate_pdf(
                overall_risk=overall_risk,
                total_clauses=len(clause_results)
            )
            with open(pdf_path, "rb") as f:
                st.download_button(
                    label="Download PDF",
                    data=f,
                    file_name="contract_risk_summary.pdf",
                    mime="application/pdf"
                )

