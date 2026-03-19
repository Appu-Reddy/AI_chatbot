import json
import os
from fastapi import FastAPI # type: ignore
from fastapi.middleware.cors import CORSMiddleware # type: ignore
from pydantic import BaseModel
from typing import List, Optional
import google.generativeai as genai # type: ignore
from dotenv import load_dotenv # type: ignore

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

    for filler in [
        "how do i", "how to", "how can i", "how do you",
        "i want to", "i would like to", "i need to", "i wish to",
        "can you", "could you", "please", "where is", "where can i",
        "show me", "take me to", "navigate to", "go to",
        "what is", "tell me", "help me",
    ]:
        q = q.replace(filler, "")

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
"""
    else:
        dom_context = "NOTE: No DOM snapshot provided."

    available_flows = get_flow_descriptions()

    prompt = f"""
You are an in-app assistant for a web application.

{dom_context}

AVAILABLE ACTION FLOWS IN THE APP:
{available_flows}

USER'S MESSAGE: "{query}"

INSTRUCTIONS:
-------------
A) If the user wants to PERFORM a simple action (create report, fill form, view dashboard,
   give feedback, get help), respond with ONLY one of these exact intent keys, nothing else:
       create_report
       fill_form
       view_dashboard
       provide_feedback
       get_help

B) If the user is asking a DETAILED QUESTION about how to use a feature, what fields exist,
   or needs step-by-step guidance based on the DOM — respond with a JSON array of steps.
   Each step must have:
     - "text": instruction for the user
     - "selector": a CSS selector from the DOM that highlights the relevant element.
                   Look for id, class, or element type in the DOM snapshot above.
                   Use "#id-name" for IDs, ".class-name" for classes, or "button", "input" etc.
                   Use "" if no specific element applies to this step.

   Example format (respond with ONLY this JSON, no extra text):
   [
     {{"text": "Click the Forms tab in the sidebar", "selector": "#forms-tab"}},
     {{"text": "You will see a Title input field", "selector": "#title"}},
     {{"text": "Fill in the Description field", "selector": "#description"}},
     {{"text": "Click the Submit Form button", "selector": "#submit-btn"}}
   ]

C) If the user is asking a GENERAL question about the app (what is this, what can I do),
   give a short friendly plain text answer in 1-2 sentences.

RULES:
- For type B questions, ALWAYS return a JSON array of steps, never plain text.
- For type B, extract real selectors from the DOM — look at id and class attributes.
- Never invent selectors that are not in the DOM.
- Never add markdown formatting outside the JSON.
- Never explain your reasoning.
- Plain text only for type C answers.
"""

    print(f"\n[gemini] Sending query to Gemini: '{query}'")
    if dom:
        print(f"[gemini] DOM snapshot length: {len(dom)} chars")

    try:
        response = model.generate_content(prompt)
        raw = response.text.strip()
        print(f"[gemini] Raw response: '{raw}'")

        raw_lower = raw.lower()

        # Check if it's a plain intent key
        for intent_key in flows_data.keys():
            if raw_lower.strip() == intent_key:
                print(f"[gemini] Detected intent: {intent_key}")
                return {"type": "intent", "value": intent_key}

        # Check if it's a JSON steps array
        if raw.startswith("["):
            try:
                clean = raw
                if "```" in clean:
                    clean = clean.split("```")[1]
                    if clean.startswith("json"):
                        clean = clean[4:]
                steps = json.loads(clean.strip())
                if isinstance(steps, list):
                    print(f"[gemini] Detected structured steps: {len(steps)} steps")
                    return {"type": "steps", "value": steps}
            except json.JSONDecodeError:
                print(f"[gemini] Failed to parse JSON steps")

        # Plain text answer
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

    # Predefined flow intent
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

    # Gemini-generated structured steps from DOM
    if result["type"] == "steps":
        steps = [
            Step(
                text=s.get('text', ''),
                selector=s.get('selector') or '',
                media=None
            )
            for s in result["value"]
        ]
        return ChatResponse(intent="guided", steps=steps)

    # Plain text answer
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