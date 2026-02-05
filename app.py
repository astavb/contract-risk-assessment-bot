import streamlit as st
from utils import extract_text, detect_language
from clause_extraction import extract_clauses
from risk_engine import detect_clause_types, assess_risk_level, contract_risk_score
from nlp_pipeline import analyze_clause
from pdf_export import generate_pdf
from audit_logger import save_audit_log

st.set_page_config(
    page_title="Contract Analysis & Risk Assessment Bot",
    layout="wide"
)

# ---------------- UI HEADER ----------------
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

# ---------------- MAIN LOGIC ----------------
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

        # ---------------- CONTRACT CLASSIFICATION ----------------
        st.subheader("Contract Classification")
        st.info("Detected Contract Type: Employment Contract")
        st.info(f"Detected language: {language}")

        # ---------------- CONTRACT OVERVIEW ----------------
        st.subheader("Contract Overview")

        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Total Clauses", len(clause_results))
        col2.metric("High Risk", risk_levels.count("High"))
        col3.metric("Medium Risk", risk_levels.count("Medium"))
        col4.metric("Low Risk", risk_levels.count("Low"))

        st.divider()

        # ---------------- CLAUSE BY CLAUSE ----------------
        st.subheader("Clause-by-Clause Analysis")

        for clause in clause_results:
            with st.container():
                risk_color = (
                    "green" if clause["risk"] == "Low"
                    else "orange" if clause["risk"] == "Medium"
                    else "red"
                )

                st.markdown(
                    f"""
                    <div style="
                        border-left: 6px solid {risk_color};
                        padding: 16px;
                        border-radius: 10px;
                        background-color: #0e1117;
                        margin-bottom: 20px;
                    ">
                        <strong>Clause {clause['id']}</strong>
                        <span style="
                            background-color: {risk_color};
                            color: white;
                            padding: 4px 10px;
                            border-radius: 14px;
                            font-size: 12px;
                            margin-left: 10px;
                        ">
                            {clause['risk']} Risk
                        </span>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

                st.markdown(clause["text"])

                st.info(clause["explanation"])

                st.markdown(
                    f"**Why it matters:** {clause['why_it_matters']}"
                )

        # ---------------- OVERALL RISK ----------------
        st.subheader("Overall Contract Risk Assessment")
        if overall_risk == "High Risk":
            st.error("High Risk Contract – urgent legal review recommended.")
        elif overall_risk == "Medium Risk":
            st.warning("Medium Risk Contract – review key clauses carefully.")
        else:
            st.success("Low Risk Contract – no major legal concerns detected.")

        # ---------------- AUDIT LOG ----------------
        audit_path = save_audit_log({
            "overall_risk": overall_risk,
            "total_clauses": len(clause_results)
        })

        st.caption(f"Audit log saved at: {audit_path}")

        # ---------------- PDF EXPORT ----------------
        if st.button("Export Risk Summary as PDF"):
            pdf_path = generate_pdf(
                overall_risk=overall_risk,
                total_clauses=len(clause_results)
            )
            st.success(f"PDF generated: {pdf_path}")



