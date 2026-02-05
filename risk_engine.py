# risk_engine.py

# Rule-based legal risk assessment engine
# Designed for explainability and SME use cases


# Clause patterns mapped to legal risk categories
RISK_PATTERNS = {
    "Penalty Clause": [
        "penalty", "fine", "liquidated damages"
    ],
    "Indemnity Clause": [
        "indemnify", "indemnification", "hold harmless"
    ],
    "Unilateral Termination": [
        "terminate at any time", "terminate without cause",
        "without notice", "immediate termination"
    ],
    "Arbitration & Jurisdiction": [
        "arbitration", "jurisdiction", "governing law",
        "courts of"
    ],
    "Auto-Renewal": [
        "auto-renew", "automatically renew"
    ],
    "Lock-in Period": [
        "lock-in", "minimum period"
    ],
    "Non-Compete": [
        "non-compete", "non compete", "restrict"
    ],
    "IP Transfer": [
        "intellectual property", "ip ownership",
        "assign all rights", "transfer of ip"
    ]
}


# Detect which legal clause types are present

def detect_clause_types(clause: str) -> list:
    clause_lower = clause.lower()
    detected = []

    for clause_type, keywords in RISK_PATTERNS.items():
        for keyword in keywords:
            if keyword in clause_lower:
                detected.append(clause_type)
                break

    return detected



# Assign risk level to an individual clause

def assess_risk_level(clause: str) -> str:
    clause_types = detect_clause_types(clause)

    # High-risk clause types for SMEs
    high_risk_types = {
        "Penalty Clause",
        "Indemnity Clause",
        "Unilateral Termination",
        "Non-Compete",
        "IP Transfer"
    }

    if any(ct in high_risk_types for ct in clause_types):
        return "High"

    if clause_types:
        return "Medium"

    return "Low"



# Compute overall contract risk
# Uses legal override logic (not just averages)

def contract_risk_score(risk_levels: list) -> str:
    """
    Legal logic:
    - 2 or more High-risk clauses => High Risk contract
    - 1 High-risk clause => Medium Risk contract
    - Otherwise fallback to weighted average
    """

    high_count = risk_levels.count("High")

    if high_count >= 2:
        return "High Risk"

    if high_count == 1:
        return "Medium Risk"

    # Fallback average-based scoring
    score_map = {"Low": 1, "Medium": 2, "High": 3}
    avg_score = sum(score_map[r] for r in risk_levels) / len(risk_levels)

    if avg_score >= 2.3:
        return "High Risk"
    elif avg_score >= 1.5:
        return "Medium Risk"
    else:
        return "Low Risk"
