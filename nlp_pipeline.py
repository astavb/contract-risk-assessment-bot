import spacy

nlp = spacy.load("en_core_web_sm")

def analyze_clause(clause):
    doc = nlp(clause)

    entities = [(ent.text, ent.label_) for ent in doc.ents
                if ent.label_ in ["ORG", "PERSON", "DATE", "MONEY", "GPE"]]

    obligations = []
    for token in doc:
        if token.lemma_ in ["shall", "must", "agree"]:
            obligations.append(token.sent.text)

    return {
        "entities": list(set(entities)),
        "obligations": list(set(obligations))
    }
