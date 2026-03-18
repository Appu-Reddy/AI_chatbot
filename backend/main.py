import json
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

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
    dom: Optional[str] = None

class Step(BaseModel):
    text: str
    selector: str
    media: Optional[str] = None

class ChatResponse(BaseModel):
    intent: str
    steps: List[Step]

with open('flows.json', 'r') as f:
    flows_data = json.load(f)

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY environment variable not set")

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-2.5-flash")

def get_flow_descriptions() -> str:
    descriptions = []
    for intent, steps in flows_data.items():
        step_text = " -> ".join([step['text'] for step in steps])
        descriptions.append(f"- {intent.replace('_', ' ').title()}: {step_text}")
    return "\n".join(descriptions)

KEYWORD_INTENTS = {
    'create_report': [
        'create report', 'generate report', 'new report', 'make report',
        'add report', 'write report', 'start report', 'build report',
    ],
    'fill_form': [
        'fill form', 'submit form', 'apply form', 'complete form',
        'create form', 'new form', 'use form', 'open form',
        'enter form', 'fill in form', 'fill out form',
        'add form', 'start form', 'filling form',
    ],
    'view_dashboard': [
        'view dashboard', 'open dashboard', 'go to dashboard', 'show dashboard',
        'see dashboard', 'check dashboard', 'visit dashboard',
    ],
    'provide_feedback': [
        'give feedback', 'leave feedback', 'submit feedback', 'send feedback',
        'add feedback', 'write feedback', 'provide feedback',
        'rate app', 'rate website', 'rate this', 'leave rating', 'give rating',
        'give stars', 'leave review',
    ],
    'get_help': [
        'get help', 'open help', 'go to help', 'show help', 'view help',
        'need help', 'want help', 'find help', 'help center', 'help page',
        'faq', 'contact support',
    ],
}

def fast_keyword_match(query: str) -> Optional[str]:
    q = query.lower().strip()

    # Strip filler phrases (full phrases only, never single letters)
    for filler in [
        "how do i", "how to", "how can i", "how do you",
        "i want to", "i would like to", "i need to", "i wish to",
        "can you", "could you", "please", "where is", "where can i",
        "show me", "take me to", "navigate to", "go to",
        "what is", "tell me", "help me",
    ]:
        q = q.replace(filler, "")

    # Strip small joining words with spaces (whole words only)
    for word in [" a ", " an ", " the ", " my ", " this ", " that "]:
        q = q.replace(word, " ")

    q = " ".join(q.split())
    print(f"[keyword] Normalized query: '{q}'")

    for intent, phrases in KEYWORD_INTENTS.items():
        for phrase in phrases:
            if phrase in q:
                print(f"[keyword match] '{phrase}' -> {intent}")
                return intent
    return None


def detect_intent_with_gemini(query: str, dom: Optional[str] = None) -> dict:
    matched_intent = fast_keyword_match(query)
    if matched_intent:
        return {"type": "intent", "value": matched_intent}

    dom_context = ""
    if dom:
        cleaned_dom = dom.strip()[:5000]
        dom_context = f"""
CURRENT PAGE DOM (live HTML snapshot from the frontend):
=========================================================
{cleaned_dom}
=========================================================
Use this DOM as your ONLY source of truth for answering questions about
what fields, buttons, labels, or content exist on the current page.
"""
    else:
        dom_context = """
NOTE: No DOM snapshot was provided for this request.
If the user asks about specific UI elements, let them know you can only
answer accurately when viewing the relevant page.
"""

    available_flows = get_flow_descriptions()

    prompt = f"""
You are an in-app assistant for a web application. Your job is to understand
what the user needs and respond appropriately.

{dom_context}

AVAILABLE ACTION FLOWS IN THE APP:
{available_flows}

USER'S MESSAGE: "{query}"

INSTRUCTIONS:
-------------
A) If the user wants to PERFORM an action (navigate somewhere, create something,
   fill something, give feedback, get help), respond with ONLY one of these exact
   intent keys and nothing else:
       create_report
       fill_form
       view_dashboard
       provide_feedback
       get_help

B) If the user is asking a QUESTION about specific UI elements, page content,
   or what exists on the page, read the DOM snapshot above carefully and extract
   the answer from it. Base your answer ONLY on what is actually present in the DOM.
   Do NOT invent or assume field names that are not in the DOM.

C) If the user is asking a GENERAL question about the app, give a short friendly
   1-2 sentence answer based on the available action flows listed above.

RULES:
- Never return an intent key for informational questions.
- Never add markdown, bullet points, asterisks, or any formatting, plain text only.
- Never invent UI elements that are not in the DOM.
- Never explain your reasoning.
- Be concise. One short paragraph max.
"""

    print(f"\n[gemini] Sending query to Gemini: '{query}'")
    if dom:
        print(f"[gemini] DOM snapshot length: {len(dom)} chars")

    try:
        response = model.generate_content(prompt)
        raw = response.text.strip()
        print(f"[gemini] Raw response: '{raw}'")

        raw_lower = raw.lower()
        for intent_key in flows_data.keys():
            if intent_key in raw_lower:
                print(f"[gemini] Detected intent: {intent_key}")
                return {"type": "intent", "value": intent_key}

        print(f"[gemini] Returning as direct answer")
        return {"type": "answer", "value": raw}

    except Exception as e:
        print(f"[gemini] Error: {e}")
        return {
            "type": "answer",
            "value": "Sorry, I ran into an issue processing your request. Please try again."
        }

@app.post("/api/chat", response_model=ChatResponse)
async def chat_endpoint(req: ChatRequest):
    result = detect_intent_with_gemini(query=req.query, dom=req.dom)

    if result["type"] == "intent":
        intent = result["value"]
        if intent in flows_data:
            steps = [
                Step(
                    text=step.get('text', ''),
                    selector=step.get('selector') or '',
                    media=step.get('media')
                )
                for step in flows_data[intent]
            ]
            return ChatResponse(intent=intent, steps=steps)

    return ChatResponse(
        intent="general",
        steps=[
            Step(
                text=result["value"].replace("\n", " ").strip(),
                selector="",
                media=None
            )
        ]
    )

@app.get("/api/health")
async def health_check():
    try:
        test_response = model.generate_content("Say 'OK' if you can read this.")
        return {
            "status": "healthy",
            "gemini_response": test_response.text.strip()
        }
    except Exception as e:
        return {
            "status": "error",
            "message": f"Gemini API error: {str(e)}"
        }

@app.get("/api/debug")
async def debug_intent(query: str = "what fields does the form have?", dom: Optional[str] = None):
    print("\n" + "=" * 60)
    print(f"DEBUG query: '{query}'")
    print("=" * 60)

    result = detect_intent_with_gemini(query=query, dom=dom)

    print(f"Result: {result}")
    print("=" * 60 + "\n")

    return {
        "query": query,
        "result": result,
        "valid_flows": list(flows_data.keys())
    }