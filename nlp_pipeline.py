import spacy

# Safe loader for local + cloud
def load_nlp():
    try:
        # Try loading full English model
        return spacy.load("en_core_web_sm")
    except Exception:
        # Fallback for Streamlit Cloud
        return spacy.blank("en")

nlp = load_nlp()

def analyze_clause(text):
    """
    Analyze a single clause using spaCy.
    Returns detected named entities and basic linguistic signals.
    """
    if not text or not text.strip():
        return {
            "entities": [],
            "has_obligation": False,
            "has_prohibition": False,
            "has_right": False
        }

    doc = nlp(text)

    # Named Entity Recognition
    entities = []
    for ent in doc.ents:
        entities.append((ent.text, ent.label_))

    # Simple rule-based legal signal detection
    text_lower = text.lower()

    obligation_keywords = ["shall", "must", "is required to", "has to"]
    prohibition_keywords = ["shall not", "must not", "is prohibited", "may not"]
    right_keywords = ["may", "is entitled to", "has the right to"]

    has_obligation = any(k in text_lower for k in obligation_keywords)
    has_prohibition = any(k in text_lower for k in prohibition_keywords)
    has_right = any(k in text_lower for k in right_keywords)

    return {
        "entities": entities,
        "has_obligation": has_obligation,
        "has_prohibition": has_prohibition,
        "has_right": has_right
    }
