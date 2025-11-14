# app/qa.py
import re
import spacy
from typing import Optional, Dict, Any

_nlp = spacy.load("en_core_web_sm")

def extract_when(text: str) -> Optional[str]:
    doc = _nlp(text)

    # 1 — DATE entities
    dates = [ent.text for ent in doc.ents if ent.label_ in ("DATE", "TIME")]
    if dates:
        return dates[0]

    # 2 — detect month phrases
    months = [
        "january","february","march","april","may","june",
        "july","august","september","october","november","december"
    ]
    lower = text.lower()

    for month in months:
        if month in lower:
            m = re.search(rf"(next\s+)?{month}(\s+\d{{1,2}})?(\s+\d{{4}})?",
                          lower, re.IGNORECASE)
            if m:
                return m.group(0).title()
            return month.title()

    # 3 — vague date phrases
    m = re.search(
        r"\b(this|next|last)\s+(week|month|year|friday|saturday|sunday|monday|tuesday|wednesday|thursday)\b",
        text,
        re.IGNORECASE
    )
    if m:
        return m.group(0)

    return None


def extract_how_many(text: str) -> Optional[str]:
    m = re.search(r"\b\d+\b", text)
    return m.group(0) if m else None
