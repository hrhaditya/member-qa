from typing import List
from rapidfuzz import fuzz

def can_answer_question(question: str, messages: List[dict]) -> dict:
    """
    Classifies whether the dataset contains enough information
    to answer the question.
    """

    q_lower = question.lower()

    # 1. Search for any name mentioned in the dataset
    names = list({msg.get("user_name", "").lower() for msg in messages})

    matched_names = [n for n in names if n in q_lower]

    # 2. Keyword match (request verbs or known patterns)
    keywords = [
        "book", "reserve", "get", "update", "confirm",
        "preference", "charge", "payment", "itinerary",
        "trip", "flight", "reservation", "status"
    ]
    keyword_hit = any(kw in q_lower for kw in keywords)

    # 3. Fuzzy content match
    best_score = 0
    for msg in messages:
        score = fuzz.partial_ratio(q_lower, msg["message"].lower())
        best_score = max(best_score, score)

    # RULE LOGIC
    if best_score >= 70 or matched_names:
        return {
            "answerable": True,
            "reason": "Found strong match in dataset"
        }

    if keyword_hit:
        return {
            "answerable": False,
            "reason": "Question mentions known action but dataset has no record"
        }

    return {
        "answerable": False,
        "reason": "Question requires reasoning or knowledge not present in dataset"
    }
