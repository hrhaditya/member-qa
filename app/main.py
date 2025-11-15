from fastapi import FastAPI
from app.schemas import AskRequest, AskResponse
from app.nlp import parse_question
from app.index import INDEX
from app.qa import extract_when, extract_how_many

app = FastAPI(
    title="Member-QA API",
    description="Ask natural-language questions about member messages.",
    version="1.0.0"
)

# ---------------------------------------------------------
# ROOT ENDPOINT (Fixes the 'Not Found' issue on Render)
# ---------------------------------------------------------
@app.get("/")
def root():
    return {
        "status": "ok",
        "message": "Member-QA API is running. Use POST /ask to query."
    }


# ---------------------------------------------------------
# MAIN QUESTION-ANSWERING ENDPOINT
# ---------------------------------------------------------
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

    # fallback: full message as answer
    return AskResponse(
        answer=msg,
        evidence={
            "user": best.get("user_name"),
            "timestamp": best.get("timestamp"),
            "message": msg
        }
    )


# ---------------------------------------------------------
# DEBUGGING ENDPOINT
# ---------------------------------------------------------
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
