def assess_risk(clause_text):
    """
    Assigns a risk level (High / Medium / Low) to a clause
    using rule-based legal risk indicators.
    """

    if not clause_text or not clause_text.strip():
        return "Low"

    text = clause_text.lower()

    high_risk_terms = [
        "indemnify",
        "penalty",
        "liquidated damages",
        "terminate immediately",
        "unilateral termination",
        "non-compete",
        "exclusive jurisdiction",
        "arbitration binding",
        "intellectual property transfer"
    ]

    medium_risk_terms = [
        "terminate",
        "arbitration",
        "jurisdiction",
        "confidentiality",
        "liability",
        "breach",
        "auto-renewal",
        "lock-in"
    ]

    for term in high_risk_terms:
        if term in text:
            return "High"

    for term in medium_risk_terms:
        if term in text:
            return "Medium"

    return "Low"
