import streamlit as st
from utils import extract_text, detect_language
from clause_extraction import extract_clauses
from nlp_pipeline import analyze_clause
from risk_engine import assess_risk
from pdf_export import generate_pdf
from audit_logger import log_audit
import os


# Page Config

st.set_page_config(
    page_title="Contract Analysis & Risk Assessment Bot",
    layout="wide"
)


# Header UI

st.markdown("""
<h1 style='text-align:center;'>Contract Analysis & Risk Assessment Bot</h1>
<p style='text-align:center; color:gray;'>
GenAI-powered legal risk assistant for Indian SMEs
</p>
""", unsafe_allow_html=True)

st.markdown("---")


# Upload Section

uploaded_file = st.file_uploader(
    "Upload your contract (PDF, DOCX, TXT)",
    type=["pdf", "docx", "txt"]
)

st.caption("Files are processed locally. No data is shared.")
st.warning("This tool provides automated risk insights for informational purposes only and does not constitute legal advice.")


# Main Logic

if uploaded_file:
    with st.spinner("Reading contract..."):
        text = extract_text(uploaded_file)
        language = detect_language(text)

    st.info(f"Detected language: {language}")

    clauses = extract_clauses(text)

    if not clauses:
        st.error("No clauses detected in the document.")
        st.stop()

    clause_results = []
    risk_counts = {"High": 0, "Medium": 0, "Low": 0}

   
    # Analyze Each Clause
  
    for idx, clause in enumerate(clauses, start=1):
        nlp_result = analyze_clause(clause)
        risk = assess_risk(clause)

        risk_counts[risk] += 1

        clause_results.append({
            "index": idx,
            "text": clause,
            "risk": risk,
            "entities": nlp_result.get("entities", []),
            "has_obligation": nlp_result.get("has_obligation", False),
            "has_prohibition": nlp_result.get("has_prohibition", False),
            "has_right": nlp_result.get("has_right", False)
        })

    
    # Overview Section
   
    st.markdown("## Contract Overview")

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Clauses", len(clauses))
    col2.metric("High Risk", risk_counts["High"])
    col3.metric("Medium Risk", risk_counts["Medium"])
    col4.metric("Low Risk", risk_counts["Low"])

    st.markdown("---")

   
    # Clause-by-Clause UI
  
    st.markdown("## Clause-by-Clause Analysis")

    for result in clause_results:
        risk_color = {
            "High": "red",
            "Medium": "orange",
            "Low": "green"
        }[result["risk"]]

        with st.expander(f"Clause {result['index']} | {result['risk']} Risk"):
            st.markdown(f"<b>Clause Text</b><br>{result['text']}", unsafe_allow_html=True)

            st.markdown(f"<br><b>Risk Level:</b> <span style='color:{risk_color}'>{result['risk']}</span>", unsafe_allow_html=True)

            # Plain-English Explanation
            if result["risk"] == "High":
                st.error("This clause may create significant legal or financial exposure and should be reviewed carefully.")
            elif result["risk"] == "Medium":
                st.warning("This clause may have moderate implications depending on enforcement.")
            else:
                st.success("This clause appears informational and does not pose immediate legal risk.")

            # Obligations / Rights / Prohibitions
            st.markdown("**Legal Signals Detected:**")
            signals = []
            if result["has_obligation"]:
                signals.append("Obligation")
            if result["has_prohibition"]:
                signals.append("Prohibition")
            if result["has_right"]:
                signals.append("Right")

            if signals:
                st.write(", ".join(signals))
            else:
                st.write("None")

            # Named Entities
            if result["entities"]:
                st.markdown("**Named Entities:**")
                for ent, label in result["entities"]:
                    st.write(f"- {ent} ({label})")

 
    # Overall Risk
  
    st.markdown("---")
    st.markdown("## Overall Contract Risk Assessment")

    if risk_counts["High"] > 0:
        overall_risk = "High Risk"
        st.error("High Risk Contract – immediate legal review recommended.")
    elif risk_counts["Medium"] > 0:
        overall_risk = "Medium Risk"
        st.warning("Medium Risk Contract – review key clauses carefully.")
    else:
        overall_risk = "Low Risk"
        st.success("Low Risk Contract – no major legal concerns detected.")

   
    # Audit Log
   
    audit_path = log_audit({
        "total_clauses": len(clauses),
        "risk_counts": risk_counts,
        "overall_risk": overall_risk
    })

    st.caption(f"Audit log saved at: {audit_path}")


    # PDF Export
    
    if st.button("Export Risk Summary as PDF"):
        pdf_path = generate_pdf(
            overall_risk=overall_risk,
            total_clauses=len(clauses)
        )
        with open(pdf_path, "rb") as f:
            st.download_button(
                label="Download PDF",
                data=f,
                file_name="contract_risk_summary.pdf",
                mime="application/pdf"
            )

