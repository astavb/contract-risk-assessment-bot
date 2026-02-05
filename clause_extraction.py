import re

def extract_clauses(text):
    raw = re.split(r"\n\d+\.|\n[A-Z][A-Za-z ]+:", text)
    return [c.strip() for c in raw if len(c.strip()) > 50]
