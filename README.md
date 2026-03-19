# In-App Product Chatbot

A smart in-app chatbot that guides users through your web application using live DOM analysis and AI. Ask it anything about the app — it highlights UI elements, gives step-by-step guidance, and answers questions about what's on screen.

---

## What It Does

- Guides users step-by-step through app features with UI element highlighting
- Reads the live page DOM to understand exactly what's on screen
- Answers questions about specific fields, buttons, and page content
- Uses AI (Gemini) only when needed — common action queries are handled instantly via keyword matching
- Highlights relevant UI elements with a "Show me where" button on each step

---

## Tech Stack

| Layer | Technology |
|---|---|
| Frontend | React 18 + Vite |
| Backend | FastAPI (Python 3.12) |
| AI | Google Gemini 2.5 Flash |
| Styling | CSS Variables + Tailwind |
| Backend Deployment | Railway |
| Frontend Deployment | Vercel |

---

## Project Structure

```
chatbot/
├── backend/
│   ├── main.py              # FastAPI app — intent detection, Gemini integration
│   ├── flows.json           # Predefined step flows for common actions
│   ├── requirements.txt     # Python dependencies
│   ├── railway.toml         # Railway deployment config
│   ├── Procfile             # Process file (fallback)
│   └── .env                 # Local environment variables (not committed)
│
├── frontend/
│   ├── public/
│   │   └── favicon.svg
│   ├── src/
│   │   ├── components/
│   │   │   └── Chatbot.jsx  # Chatbot UI — DOM capture, step rendering, highlighting
│   │   ├── pages/
│   │   │   ├── Dashboard.jsx
│   │   │   ├── Reports.jsx
│   │   │   ├── Forms.jsx
│   │   │   ├── Help.jsx
│   │   │   └── Feedback.jsx
│   │   ├── App.jsx
│   │   ├── App.css
│   │   └── main.jsx
│   ├── index.html
│   ├── vite.config.js
│   ├── vercel.json          # Vercel SPA routing config
│   └── package.json
│
└── README.md
```

---

## How It Works

```
User sends a message
        ↓
Keyword match found?
  YES → Return predefined steps instantly (no API call, free)
        ↓ NO
Send query + live DOM snapshot to Gemini
        ↓
Gemini returns structured JSON steps with CSS selectors?
  YES → Render as guided steps with "Show me where" buttons
        ↓ NO
Gemini returns plain text?
  YES → Show as a direct answer message
```

### DOM Snapshot

Every message captures a snapshot of the current page's HTML (up to 5000 chars, noise stripped) and sends it to the backend. Gemini reads this to find real field names, button labels, and CSS selectors — so answers are always based on what's actually on screen, not hardcoded assumptions.

---

## Getting Started

### Prerequisites

- Node.js 18+
- Python 3.10+
- Google Gemini API key → [Get one here](https://ai.google.dev)

---

### Backend Setup

```bash
cd backend

# Create and activate virtual environment
python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # Mac/Linux

# Install dependencies
pip install -r requirements.txt
```

Create a `.env` file in the `backend/` folder:
```
GEMINI_API_KEY=your_key_here
```

Start the server:
```bash
uvicorn main:app --port 8001 --reload
```

The backend runs at `http://localhost:8001`

---

### Frontend Setup

```bash
cd frontend
npm install
```

Create a `.env` file in the `frontend/` folder:
```
VITE_API_URL=http://localhost:8001/api/chat
```

Start the dev server:
```bash
npm run dev
```

The frontend runs at `http://localhost:5173`

---

## Adding New Flows

### Step 1 — Add steps to `flows.json`

```json
{
  "your_intent_name": [
    { "text": "Step 1 description", "selector": "#element-id" },
    { "text": "Step 2 description", "selector": ".class-name" },
    { "text": "Step 3 description", "selector": "" }
  ]
}
```

### Step 2 — Add keywords to `main.py`

```python
KEYWORD_INTENTS = {
    ...
    'your_intent_name': [
        'keyword phrase one', 'keyword phrase two'
    ],
}
```

That's it. The chatbot will now recognize the new flow and highlight the correct elements.

---

## API Reference

| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/api/chat` | Main chat endpoint |
| `GET` | `/api/health` | Verify Gemini API is working |
| `GET` | `/api/debug?query=...` | Test intent detection without frontend |

### POST `/api/chat`

Request body:
```json
{
  "query": "what fields does the form have",
  "dom": "<div class=\"page-container\">...</div>"
}
```

Response:
```json
{
  "intent": "guided",
  "steps": [
    { "text": "Navigate to the Forms tab", "selector": "#forms-tab", "media": null },
    { "text": "You will see a Title input field", "selector": "#title", "media": null },
    { "text": "Fill in the Description textarea", "selector": "#description", "media": null },
    { "text": "Click Submit Form to submit", "selector": "#submit-btn", "media": null }
  ]
}
```

Intent values: `create_report`, `fill_form`, `view_dashboard`, `provide_feedback`, `get_help`, `guided`, `general`

---

## Deployment

### Backend — Railway

1. Push the `backend/` folder to a GitHub repo
2. Create a new project on [Railway](https://railway.app) and connect the repo
3. Set the root directory to `backend/`
4. Add environment variable in Railway dashboard: `GEMINI_API_KEY=your_key_here`
5. Railway uses `railway.toml` to run the server automatically

`railway.toml`:
```toml
[deploy]
startCommand = "uvicorn main:app --host 0.0.0.0 --port 8001"
```

### Frontend — Vercel

1. Push the `frontend/` folder to a GitHub repo
2. Import the repo on [Vercel](https://vercel.com)
3. Set the root directory to `frontend/`
4. Add environment variable: `VITE_API_URL=https://your-railway-url.up.railway.app/api/chat`
5. Deploy

`vercel.json` handles SPA routing so React Router works correctly on refresh.

---

## Environment Variables

| Variable | Where | Description |
|---|---|---|
| `GEMINI_API_KEY` | Backend `.env` / Railway | Your Google Gemini API key |
| `VITE_API_URL` | Frontend `.env` / Vercel | Full URL to the backend `/api/chat` endpoint |

---

## Test Queries

### Instant (keyword match — no API call)

```
how to fill a form
how to create a report
i want to give feedback
i need help
view the dashboard
complete the form
generate a report
submit feedback
```

### Guided steps with UI highlighting (Gemini + DOM)

```
what fields does the form have
give me detailed steps to fill the form
walk me through submitting the form
explain how to use the feedback section
what do i need to fill in here
guide me through creating a report
```

### Plain answers (Gemini general)

```
what is this app
what can i do here
i am a new user
what features does this app have
```

### Debug URLs (test in browser)

```
http://localhost:8001/api/health
http://localhost:8001/api/debug?query=how+to+fill+a+form
http://localhost:8001/api/debug?query=what+fields+does+the+form+have
http://localhost:8001/api/debug?query=what+is+this+app
http://localhost:8001/api/debug?query=asdfghjkl
```

---

## How the DOM Capture Works

The `captureDomSnapshot()` function in `Chatbot.jsx`:

1. Clones `document.body` so the live page is not affected
2. Strips `<script>`, `<style>`, `<noscript>`, `<svg>`, `.chatbot-widget`, and `[aria-hidden]` elements
3. Targets only the main content area (`main`, `.main-content`, `#root`) to reduce payload size
4. Collapses whitespace and caps at 5000 characters
5. Sends the cleaned HTML string to the backend with every message

Gemini then reads the real `id` and `class` attributes from this snapshot to extract field names and build CSS selectors for the "Show me where" highlighting.

---

## Gemini API Notes

- Model used: `gemini-2.5-flash`
- Free tier limit: 20 requests per minute
- Keyword-matched queries (the majority of action queries) never hit the API
- Only ambiguous or informational queries call Gemini

---

## Known Limitations

- DOM snapshot is capped at 5000 characters — very long pages may be truncated
- If the user is on a different page than the one they're asking about, Gemini reads the current page's DOM only
- Gemini-generated selectors depend on the quality of the DOM snapshot — elements without `id` or `class` may get generic selectors