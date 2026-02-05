import re


def split_into_clauses(text: str) -> list:
    """
    Split contract text into meaningful clauses.
    """

    if not text:
        return []

    # Normalize whitespace
    text = re.sub(r"\n+", "\n", text)

    # Split by legal markers
    patterns = [
        r"\n\d+\.\s",
        r"\nSection\s+\d+",
        r"\nClause\s+\d+",
        r"\n[A-Z][A-Z\s]{6,}\n"
    ]

    split_regex = "|".join(patterns)
    parts = re.split(split_regex, text)

    clauses = []
    for p in parts:
        p = p.strip()
        if len(p) > 40:
            clauses.append(p)

    return clauses
