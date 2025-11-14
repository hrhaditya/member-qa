# app/client.py
import json
from pathlib import Path
from typing import List, Dict, Any

DATA_PATH = Path(__file__).resolve().parent.parent / "data" / "messages.json"


def fetch_all_messages() -> List[Dict[str, Any]]:
    """
    Load all messages from the local JSON file.

    The file has the shape:
    {
        "total": 3349,
        "items": [ {...}, {...}, ... ]
    }
    """
    with DATA_PATH.open(encoding="utf-8") as f:
        data = json.load(f)

    items = data.get("items", data)  # safety: if it's already a list

    cleaned: List[Dict[str, Any]] = []
    for item in items:
        if isinstance(item, dict):
            cleaned.append(item)
        elif isinstance(item, str):
            # Fallback: wrap plain strings in a dict so the rest of the code never breaks
            cleaned.append({
                "message": item,
                "user_name": "",
                "timestamp": "",
            })
        else:
            # ignore weird entries
            continue

    return cleaned
