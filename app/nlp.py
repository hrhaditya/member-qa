# app/nlp.py
import spacy
from typing import List, Optional
from app.schemas import ParsedQuestion

nlp = spacy.load("en_core_web_sm")

def parse_question(text: str) -> ParsedQuestion:
    doc = nlp(text)

    detected_name = None
    qtype = None
    keywords: List[str] = []

    # Step 1 — detect PERSON entity
    for ent in doc.ents:
        if ent.label_ == "PERSON":
            detected_name = ent.text
            break

    # Step 2 — fallback: detect capitalized word
    if not detected_name:
        for tok in doc:
            if tok.text[0].isupper() and tok.text.isalpha():
                detected_name = tok.text
                break

    # Step 3 — detect question type
    lower = text.lower()
    if "when" in lower:
        qtype = "when"
    elif "how many" in lower:
        qtype = "how_many"
    else:
        qtype = "other"

    # Step 4 — keyword extraction (excluding the name)
    for tok in doc:
        if not tok.is_stop and tok.is_alpha:
            if detected_name and tok.text.lower() == detected_name.lower():
                continue
            keywords.append(tok.text.lower())

    # Step 5 — add locations as keywords
    for ent in doc.ents:
        if ent.label_ in ("GPE", "LOC"):
            keywords.append(ent.text.lower())

    return ParsedQuestion(
        name=detected_name,
        qtype=qtype,
        keywords=list(set(keywords))  # dedupe
    )
