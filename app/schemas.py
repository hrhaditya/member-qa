# app/schemas.py
from pydantic import BaseModel
from typing import List, Optional, Dict, Any

class ParsedQuestion(BaseModel):
    name: Optional[str]
    qtype: str
    keywords: List[str]

class AskRequest(BaseModel):
    question: str

class AskResponse(BaseModel):
    answer: str
    evidence: Dict[str, Any]
