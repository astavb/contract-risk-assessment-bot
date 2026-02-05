import re


def extract_clauses(text: str) -> list:
    """
    Splits contract text into clauses using headings,
    numbering, and paragraph breaks.
    """

    if not text:
        return []

    # Normalize text
    text = text.replace("\r", "\n")

    # Split on common clause patterns
    patterns = [
        r"\n\s*\d+\.\s+",              # 1. 2. 3.
        r"\n\s*Section\s+[A-Z0-9]+",   # Section IX
        r"\n\s*ARTICLE\s+[A-Z0-9]+",   # ARTICLE IV
        r"\n\s*\([a-z]\)\s+",          # (a) (b)
        r"\n\s*\n+"                    # blank lines
    ]

    split_regex = "|".join(patterns)
    raw_clauses = re.split(split_regex, text)

    # Clean clauses
    clauses = []
    for clause in raw_clauses:
        clause = clause.strip()
        if len(clause) > 50:  # ignore very small junk text
            clauses.append(clause)

    return clauses

