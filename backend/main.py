import json
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables from .env file
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

# Configure Gemini API
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)
    model = genai.GenerativeModel("gemini-2.5-flash")
else:
    raise ValueError("GEMINI_API_KEY environment variable not set")

def get_flow_descriptions() -> str:
    """Generate a description of all available flows for the AI context"""
    descriptions = []
    for intent, steps in flows_data.items():
        step_text = " → ".join([step['text'] for step in steps])
        descriptions.append(f"- {intent.replace('_', ' ').title()}: {step_text}")
    return "\n".join(descriptions)

def get_frontend_structure() -> str:
    """Get the frontend structure to help AI understand UI elements"""
    frontend_structure = """
FRONTEND STRUCTURE:
==================
The application has a sidebar navigation with the following tabs/pages:

1. Dashboard (#dashboard-tab)
   - Route: /
   - Purpose: Overview of app activity
   - Features: Activity summaries, statistics

2. Reports (#reports-tab)
   - Route: /reports
   - Purpose: Create and manage reports
   - Features: Create report button, report list

3. Forms (#forms-tab)
   - Route: /forms
   - Purpose: Fill and submit forms
   - Features: Form fields, submit button

4. Help Center (#help-tab)
   - Route: /help
   - Purpose: FAQ and support documentation
   - Features: Help articles, search

5. Give Feedback (#feedback-tab)
   - Route: /feedback
   - Purpose: User feedback and ratings
   - Features: Star rating, feedback text, submit button

The chatbot widget provides step-by-step guidance with:
- Text instructions
- Element highlighting (via CSS selectors)
- Media/GIFs for visual guidance
"""
    return frontend_structure

def detect_intent_with_gemini(query: str) -> str:
    """Use Gemini API to intelligently detect user intent based on query and available flows"""
    
    query_lower = query.lower()

    # Normalize common phrases
    query_lower = query_lower.replace("i want to", "")
    query_lower = query_lower.replace("i would like to", "")
    query_lower = query_lower.replace("how do i", "")
    query_lower = query_lower.replace("how to", "")
    query_lower = query_lower.strip()
    
    # FAST keyword-based matching first (no API call)
    keyword_intents = {
        'create_report': ['create report', 'generate report', 'new report', 'report'],
        'fill_form': ['fill form', 'submit form', 'apply form', 'form'],
        'view_dashboard': ['dashboard', 'overview', 'statistics'],
        'provide_feedback': [
            'feedback',
            'rating',
            'review',
            'rate',
            'rate website',
            'rate app',
            'give feedback',
            'leave feedback'
        ],
        'get_help': ['help', 'assistance', 'faq', 'support']
    }
    
    # Check for keyword matches
    for intent, keywords in keyword_intents.items():
        for keyword in keywords:
            if keyword in query_lower:
                print(f"\nQuery: {query}")
                print(f"Matched keyword: '{keyword}'")
                print(f"Detected Intent: {intent}\n")
                return intent
    
    # If no keyword match, use Gemini AI (fallback)
    print(f"\nQuery: {query}")
    print(f"Method: Using Gemini API (no keyword match found)")
    
    available_flows = get_flow_descriptions()
    frontend_structure = get_frontend_structure()
    
    prompt = f"""{frontend_structure}
        Available Feature Flows:
        {available_flows}

        User's Request: "{query}"

        Your job is to decide if the user is asking to DO something in the app, or asking a general question.

        RULE 1 — If the user wants to perform a specific task (create, fill, view, give feedback, get help), respond with ONLY one of these exact keys:
        create_report
        fill_form
        view_dashboard
        provide_feedback
        get_help

        RULE 2 — If the user is asking a general question (e.g. "what is this app?", "what can I do here?", "tell me about this", "I'm a new user"), respond with a SHORT, friendly 1-2 sentence answer describing the app based on the frontend structure above. Do NOT return an intent key in this case.

        Do not explain your reasoning. Do not add punctuation around intent keys. Just follow the rules."""

    try:
        response = model.generate_content(prompt)
        raw_response = response.text.strip().lower()
        
        print(f"GEMINI RESPONSE: '{raw_response}'")
        
        valid_intents = list(flows_data.keys())

        for valid_intent in valid_intents:
            if valid_intent in raw_response:
                print(f"Detected Intent: {valid_intent}\n")
                return valid_intent

        # Gemini answered a general question — return its natural response
        print(f"Detected as general response\n")
        return raw_response
        
    except Exception as e:
        print(f"Error calling Gemini API: {e}")
        print(f"Detected Intent: unknown\n")
        return 'unknown'

@app.post("/api/chat", response_model=ChatResponse)
async def chat_endpoint(req: ChatRequest):
    # Use Gemini to detect intent
    intent = detect_intent_with_gemini(req.query)
    
    if intent in flows_data:
        base_steps = flows_data[intent]
        steps = [
            Step(
                text=step.get('text', ''),
                selector=step.get('selector') or '',
                media=step.get('media')
            )
            for step in base_steps
        ]
        return ChatResponse(intent=intent, steps=steps)
    
    # Gemini answered a general question — return natural response
    else:
        return ChatResponse(
            intent="general",
            steps=[
                Step(
                    text=intent.strip().replace("\n", " "),  # clean up Gemini output
                    selector="",
                    media=None
                )
            ]
        )

@app.get("/api/health")
async def health_check():
    """Test endpoint to verify Gemini API is working"""
    try:
        test_response = model.generate_content("Say 'OK' if you can read this.")
        return {
            "status": "healthy",
            "message": "Gemini API is working",
            "gemini_response": test_response.text.strip()
        }
    except Exception as e:
        return {
            "status": "error",
            "message": f"Gemini API error: {str(e)}"
        }

@app.get("/api/debug")
async def debug_intent(query: str = "how do I create a report?"):
    """Debug endpoint to see raw Gemini response"""
    print("\n" + "="*60)
    print(f"DEBUG: Testing query: '{query}'")
    print("="*60)
    
    intent = detect_intent_with_gemini(query)
    
    print(f"Final Result: {intent}")
    print("="*60 + "\n")
    
    return {
        "query": query,
        "detected_intent": intent,
        "valid_flows": list(flows_data.keys())
    }