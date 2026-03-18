import json
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI(title="In-App Product Chatbot API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    query: str

class Step(BaseModel):
    text: str
    selector: str
    media: Optional[str] = None

class ChatResponse(BaseModel):
    intent: str
    steps: List[Step]

# Load predefined flows from JSON
with open('flows.json', 'r') as f:
    flows_data = json.load(f)

# Simple Mock LLM/Intent detection logic based on keywords
def detect_intent(query: str) -> str:
    query = query.lower()
    if 'report' in query:
        return 'create_report'
    elif 'form' in query or 'fill' in query:
        return 'fill_form'
    elif 'dashboard' in query or 'overview' in query:
        return 'view_dashboard'
    elif 'feedback' in query or 'rate' in query or 'review' in query:
        return 'provide_feedback'
    elif 'help' in query or 'support' in query or 'faq' in query:
        return 'get_help'
    return 'unknown'

@app.post("/api/chat", response_model=ChatResponse)
async def chat_endpoint(req: ChatRequest):
    intent = detect_intent(req.query)
    
    if intent in flows_data:
        steps = flows_data[intent]
        return ChatResponse(intent=intent, steps=steps)
    else:
        # Fallback response
        return ChatResponse(
            intent="unknown",
            steps=[
                Step(
                    text="I didn't quite catch that. Try asking about 'creating a report', 'filling a form', 'giving feedback', or 'getting help'.",
                    selector="",
                    media=None
                )
            ]
        )
