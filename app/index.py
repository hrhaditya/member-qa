# app/index.py
from typing import List, Dict, Any
from rapidfuzz import fuzz
from app.client import fetch_all_messages
from app.schemas import ParsedQuestion

class MessageIndex:
    def __init__(self):
        self.messages: List[Dict[str, Any]] = []

    def load(self, msgs: List[Dict[str, Any]]):
        self.messages = msgs

    def search_messages(self, parsed: ParsedQuestion) -> List[Dict[str, Any]]:
        # Step 1 — filter by detected name
        if parsed.name:
            msgs = [
                m for m in self.messages
                if parsed.name.lower() in m.get("user_name", "").lower()
            ]
        else:
            msgs = self.messages

        results = []

        # Step 2 — score messages
        for m in msgs:
            text = m.get("message", "").lower()
            score = 0

            # keyword scoring
            for kw in parsed.keywords:
                if kw.lower() in text:
                    score += 2

            # fuzzy score
            s = fuzz.partial_ratio(" ".join(parsed.keywords), text)
            score += s / 50  # reduce weight

            # date hint scoring
            if parsed.qtype == "when":
                if any(x in text for x in ["on ", "at ", "next", "tomorrow", "friday", "saturday"]):
                    score += 3

            if score > 0:
                m["_score"] = score
                results.append(m)

        # Step 3 — sort highest first
        results.sort(key=lambda x: x["_score"], reverse=True)
        return results


# Build index once
ALL_MESSAGES = fetch_all_messages()
INDEX = MessageIndex()
INDEX.load(ALL_MESSAGES)
