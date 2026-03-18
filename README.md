# In-App Product Chatbot

( This was done as a part of a company recruitment process )

A modern, full-stack chatbot application that provides intelligent in-app product guidance and helps users navigate application features. The chatbot understands user intents and provides step-by-step visual guidance for completing tasks.

---

## 🌟 Features

- **Intelligent Intent Detection**: Automatically recognizes user queries and maps them to predefined workflows
- **Visual Step-by-Step Guidance**: Highlights UI elements and provides instructions on how to use app features
- **Multi-Page Application**: Dashboard, Reports, Forms, Feedback, and Help Center
- **Real-Time Chat Interface**: Responsive chatbot widget with conversation history
- **AI Integration Ready**: Supports Gemini API for enhanced language understanding
- **CORS-Enabled API**: Secure backend with proper cross-origin resource sharing
- **Environment-Based Configuration**: Separate development and production setups

---

## 📋 Table of Contents

- [Tech Stack](#tech-stack)
- [Project Architecture](#project-architecture)
- [Project Structure](#project-structure)
- [Prerequisites](#prerequisites)
- [Installation & Setup](#installation--setup)
- [Configuration](#configuration)
- [Running Locally](#running-locally)
- [API Documentation](#api-documentation)
- [Deployment](#deployment)
- [Usage Guide](#usage-guide)
- [Contributing](#contributing)

---

## 🛠️ Tech Stack

### Frontend
- **React 19.2** - UI library
- **Vite 8.0** - Build tool and dev server
- **React Router DOM 7.13** - Client-side routing
- **Lucide React 0.577** - Icon library
- **CSS3** - Styling with CSS custom properties

### Backend
- **FastAPI 0.111** - Modern Python web framework
- **Uvicorn 0.30** - ASGI server
- **Pydantic 2.7** - Data validation
- **Python 3.11+** - Programming language

### Deployment
- **Vercel** - Frontend hosting
- **Railway** - Backend hosting
- **GitHub** - Version control and CI/CD

---

## 🏗️ Project Architecture

```
In-App Product Chatbot
├── Frontend (React + Vite)
│   ├── Pages (Dashboard, Reports, Forms, Feedback, Help)
│   ├── Components (Chatbot Widget)
│   └── Assets & Styles
│
└── Backend (FastAPI + Python)
    ├── Chat Endpoint (/api/chat)
    ├── Intent Detection Logic
    ├── Flow Configuration (flows.json)
    └── CORS Middleware
```

### Data Flow
1. User types a message in the chatbot widget
2. Frontend sends request to `/api/chat` endpoint
3. Backend detects user intent using keyword matching
4. Backend retrieves predefined flow steps from `flows.json`
5. Backend returns steps with selectors and instructions
6. Frontend highlights UI elements and displays guidance

---

## 📁 Project Structure

```
chatbot/
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   └── Chatbot.jsx          # Main chatbot widget component
│   │   ├── pages/
│   │   │   ├── Dashboard.jsx        # Dashboard page
│   │   │   ├── Reports.jsx          # Reports page
│   │   │   ├── Forms.jsx            # Forms page
│   │   │   ├── Feedback.jsx         # Feedback page
│   │   │   └── Help.jsx             # Help center page
│   │   ├── App.jsx                  # Main app component with routing
│   │   ├── App.css                  # Main styles
│   │   ├── index.css                # Global styles
│   │   └── main.jsx                 # React entry point
│   ├── public/                      # Static assets
│   ├── package.json                 # Dependencies & scripts
│   ├── vite.config.js              # Vite configuration
│   └── vercel.json                 # Vercel deployment config
│
├── backend/
│   ├── main.py                      # FastAPI application & endpoints
│   ├── flows.json                   # Predefined workflow steps
│   ├── requirements.txt             # Python dependencies
│   ├── .env                         # Environment variables (local)
│   ├── Procfile                     # Heroku/Railway process definition
│   ├── railway.json                 # Railway deployment config
│   ├── start.sh                     # Startup script
│   └── .python-version              # Python version specification
│
└── README.md                        # This file
```

---

## 📦 Prerequisites

Before you begin, ensure you have the following installed:

### Frontend
- Node.js 18+ and npm/yarn
- Git

### Backend
- Python 3.11+
- pip or poetry
- Git

### Deployment
- Vercel account (for frontend)
- Railway account (for backend)
- GitHub account (for CI/CD)

---

## 🚀 Installation & Setup

### 1. Clone the Repository

```bash
git clone https://github.com/your-repo/chatbot.git
cd chatbot
```

### 2. Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev

# Build for production
npm run build
```

The frontend will be available at `http://localhost:5173`

### 3. Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run development server
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

The backend API will be available at `http://localhost:8000`

---

## ⚙️ Configuration

### Environment Variables

#### Backend (.env)
Create a `.env` file in the `backend/` directory:

```env
GEMINI_API_KEY=your_gemini_api_key_here
```

**Note:** The `GEMINI_API_KEY` is currently loaded but not actively used in the base implementation. It's there for future AI enhancement integration.

#### Frontend (Vite)
Environment variables for the frontend are managed through Vercel's dashboard:

- `VITE_API_URL`: The backend API URL (e.g., `https://your-railway-app.railway.app/api/chat`)

### flows.json

The `flows.json` file contains predefined workflows that the chatbot can guide users through. Example structure:

```json
{
  "create_report": [
    {
      "text": "Click the 'Create Report' button to start.",
      "selector": "#create-report-btn",
      "media": null
    },
    {
      "text": "Select your report type from the dropdown.",
      "selector": "select.report-type",
      "media": null
    }
  ],
  "fill_form": [
    {
      "text": "Fill in the form fields with your information.",
      "selector": "form.user-form",
      "media": null
    }
  ]
}
```

---

## 🏃 Running Locally

### 1. Start Backend
```bash
cd backend
source venv/bin/activate  # or venv\Scripts\activate on Windows
python -m uvicorn main:app --reload
```

### 2. Start Frontend (in a new terminal)
```bash
cd frontend
npm run dev
```

### 3. Access the Application
- Frontend: `http://localhost:5173`
- Backend API: `http://localhost:8000`
- API Docs: `http://localhost:8000/docs` (Swagger UI)

---

## 📡 API Documentation

### Chat Endpoint

**POST** `/api/chat`

Send a user query and receive guided steps for the detected intent.

#### Request
```json
{
  "query": "How do I create a report?"
}
```

#### Response
```json
{
  "intent": "create_report",
  "steps": [
    {
      "text": "Click the 'Create Report' button.",
      "selector": "#create-report-btn",
      "media": null
    },
    {
      "text": "Fill in the report details.",
      "selector": "form.report-form",
      "media": null
    }
  ]
}
```

#### Supported Intents
- `create_report` - Guides user to create a report
- `fill_form` - Guides user to fill out a form
- `view_dashboard` - Guides user to view the dashboard
- `provide_feedback` - Guides user to provide feedback
- `get_help` - Guides user to help resources
- `unknown` - Default response for unrecognized queries

#### Error Response
If the intent is unknown, the API returns:
```json
{
  "intent": "unknown",
  "steps": [
    {
      "text": "I didn't quite catch that. Try asking about 'creating a report', 'filling a form', 'giving feedback', or 'getting help'.",
      "selector": "",
      "media": null
    }
  ]
}
```

---

## 🌐 Deployment

### Frontend Deployment to Vercel

1. **Push code to GitHub**
   ```bash
   git add .
   git commit -m "Deployment ready"
   git push origin main
   ```

2. **Connect to Vercel**
   - Visit [vercel.com](https://vercel.com)
   - Click "Add New..." → "Project"
   - Import your GitHub repository
   - Set **Root Directory** to `frontend`
   - Configure **Environment Variables**:
     - `VITE_API_URL`: Your Railway backend URL

3. **Deploy**
   - Click "Deploy" button
   - Vercel will build and deploy automatically

### Backend Deployment to Railway

1. **Connect to Railway**
   - Visit [railway.app](https://railway.app)
   - Click "New Project" → "Deploy from GitHub repo"
   - Select your repository
   - Set **Root Directory** to `backend`

2. **Configure Environment Variables**
   - Go to Service Settings
   - Add `GEMINI_API_KEY` in Environment Variables

3. **Deploy**
   - Railway will automatically detect Python
   - Install dependencies from `requirements.txt`
   - Start the app using `Procfile` or `start.sh`
   - Your backend will be live at a Railway URL

### Verifying Deployment

1. **Test Backend**
   ```bash
   curl -X POST https://your-railway-app.railway.app/api/chat \
     -H "Content-Type: application/json" \
     -d '{"query": "create a report"}'
   ```

2. **Test Frontend**
   - Visit your Vercel URL
   - Open the chatbot widget
   - Test interaction with backend

---

## 💬 Usage Guide

### For Users

1. **Access the Application**: Visit your deployed Vercel frontend URL
2. **Navigate Pages**: Use the sidebar to navigate between Dashboard, Reports, Forms, Help, and Feedback
3. **Chat with Bot**: Click the chatbot icon in the bottom-right corner
4. **Ask Questions**: Type queries like:
   - "How do I create a report?"
   - "Show me how to fill out a form"
   - "How do I give feedback?"
5. **Follow Guidance**: The chatbot will highlight UI elements and guide you through tasks

### For Developers

#### Adding New Intents

1. **Update `flows.json`** with new intent and steps
2. **Update `detect_intent()` function** in `main.py` to recognize keywords
3. **Deploy** to Railway
4. **Test** using the API docs at `/docs`

#### Customizing UI Elements

1. **Modify React components** in `frontend/src/pages/` and `frontend/src/components/`
2. **Update CSS** in `frontend/src/App.css` and `frontend/src/index.css`
3. **Test locally** with `npm run dev`
4. **Push to GitHub** for automatic Vercel deployment

#### Enhancing with AI

The backend is ready to integrate with Gemini API:

```python
# In main.py, you can add:
from google.generativeai import genai

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

async def chat_endpoint(req: ChatRequest):
    # Use Gemini to enhance intent detection
    response = genai.generate_text(prompt=f"Detect intent: {req.query}")
    # ... process response
```

---

## 🤝 Contributing

Contributions are welcome! To contribute:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📝 License

This project is open source and available under the MIT License.

---

## 📧 Support

For issues, questions, or suggestions, please:
- Open an issue on GitHub
- Contact the development team
- Check the Help Center in the application

---

## 🔒 Security Notes

- **CORS**: Currently allows all origins. For production, restrict to your domain:
  ```python
  allow_origins=["https://your-vercel-domain.vercel.app"]
  ```
- **API Keys**: Never commit `.env` files with sensitive keys
- **Input Validation**: All inputs are validated using Pydantic
- **HTTPS**: Both Vercel and Railway provide HTTPS by default

---

## 📊 Performance Tips

- **Frontend**: Vite provides fast build times and optimized bundles
- **Backend**: FastAPI is built on async, handling multiple requests efficiently
- **Caching**: Consider caching flows.json on the frontend for faster interactions
- **API Optimization**: Responses are minimal and focused on essential data

---

## 🎯 Future Enhancements

- [ ] Integrate Gemini AI for natural language understanding
- [ ] Add conversation persistence (database storage)
- [ ] Implement user analytics
- [ ] Add multi-language support
- [ ] Create admin dashboard for managing flows
- [ ] Add voice command support
- [ ] Implement sentiment analysis
- [ ] Add video tutorials/media support

---

## 📚 Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [React Documentation](https://react.dev/)
- [Vite Guide](https://vitejs.dev/)
- [Railway Docs](https://docs.railway.app/)
- [Vercel Docs](https://vercel.com/docs/)

---

**Built with ❤️ by the Development Team**
