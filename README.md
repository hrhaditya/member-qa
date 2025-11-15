Member-QA: Natural Language Question Answering API
This project is a small question-answering service that can understand natural-language questions and respond with answers inferred from the Member Messages API provided in the challenge.
The API parses a user’s question, searches through member messages, extracts relevant information, and returns a clean JSON answer.

The service is implemented using FastAPI, deployed on Render, and publicly accessible.

🚀 Live API
Base URL:
https://member-qa-w3bt.onrender.com
Endpoints
1. Health Check (GET /)
Returns a simple message confirming the service is running.
2. Ask a Question (POST /ask)
Send a natural-language question and receive an inferred answer.
Example request:
{
  "question": "When is Layla planning her trip to London?"
}

How It Works
1. NLP Parsing
A lightweight natural-language parser identifies question type:
“when” questions → date extraction
“how many” questions → quantity extraction
fallback → return matched message text

2. Message Indexing
On startup, the API fetches all member messages from:
GET https://november7-730026606190.europe-west1.run.app/messages
Messages are indexed locally for:
keyword matching
simple semantic ranking
fast retrieval

3. Answer Extraction
Depending on the parsed question type, the API pulls out:
dates (for “when”)
numeric quantities (for “how many”)
or returns the raw message for descriptive questions

🛠 Running Locally
Prerequisites
Python 3.10+
pip / venv

Install & Run
pip install -r requirements.txt
uvicorn app.main:app --reload
Open your browser at:
http://localhost:8000/docs

Deployment
The API is deployed on Render Web Services using a Dockerfile.
Render automatically detects the service, exposes port 8080, and runs the FastAPI app.

Bonus Section
Bonus 1 — Design Notes (Alternatives I Considered)
I evaluated a few different approaches before settling on this solution:
✔️ 1. Full LLM-based QA
Use an LLM (GPT, Llama) to analyze messages and answer questions.
Pros: Very flexible and accurate.
Cons: Expensive, requires API keys, adds latency.
✔️ 2. Embedding-based semantic search
Generate embeddings for each message (e.g., using Sentence-BERT).
Pros: Great for fuzzy matching.
Cons: Extra infrastructure and model hosting.
✔️ 3. Rule-based + keyword matching (Chosen Approach)
Simple, fast, reliable for structured messages.
Matches keywords from the parsed question and applies extraction rules.
This approach was chosen because it's:
lightweight
deterministic
easy to evaluate
deploys quickly

Bonus 2 — Data Insights (Anomalies Noticed)
While exploring member messages, I noticed a few inconsistencies:
Some users mention events multiple times with slightly different details (e.g., trip dates differ across messages)
Names sometimes appear with typos or nicknames, causing fuzzy matching challenges
A few messages don’t match any known user format
Some messages contain multiple pieces of information, requiring careful extraction
These small inconsistencies influenced the design of the parser and extraction logic.

