# app/main.py
from fastapi import FastAPI
from app.schemas import AskRequest, AskResponse
from app.nlp import parse_question
from app.index import INDEX
from app.qa import extract_when, extract_how_many

app = FastAPI()

@app.post("/ask", response_model=AskResponse)
def ask(req: AskRequest) -> AskResponse:
    parsed = parse_question(req.question)
    print("Parsed →", parsed)

    matches = INDEX.search_messages(parsed)
    print(f"Found {len(matches)} matches")

    if not matches:
        return AskResponse(answer="No answer found.", evidence={})

    best = matches[0]
    msg = best["message"]

    # Answer extraction
    if parsed.qtype == "when":
        extracted = extract_when(msg)
        if extracted:
            return AskResponse(
                answer=extracted,
                evidence={
                    "user": best.get("user_name"),
                    "timestamp": best.get("timestamp"),
                    "message": msg
                }
            )

    if parsed.qtype == "how_many":
        extracted = extract_how_many(msg)
        if extracted:
            return AskResponse(
                answer=extracted,
                evidence={
                    "user": best.get("user_name"),
                    "timestamp": best.get("timestamp"),
                    "message": msg
                }
            )

    # fallback: full message
    return AskResponse(
        answer=msg,
        evidence={
            "user": best.get("user_name"),
            "timestamp": best.get("timestamp"),
            "message": msg
        }
    )


# debug endpoint
@app.get("/test")
def test():
    layla_messages = [
        m for m in INDEX.messages if "layla" in m.get("user_name", "").lower()
    ]
    london_messages = [
        m for m in INDEX.messages if "london" in m.get("message", "").lower()
    ]

    return {
        "total_messages": len(INDEX.messages),
        "layla_messages": len(layla_messages),
        "london_messages": len(london_messages),
        "sample_layla": layla_messages[0] if layla_messages else None
    }
