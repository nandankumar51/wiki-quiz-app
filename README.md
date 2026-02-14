# Wiki Quiz Generator

A full-stack web application that generates educational quizzes from Wikipedia articles using AI (Google Gemini). Built with FastAPI backend and React frontend.

## 📋 Table of Contents

- [Features](#features)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Running the Application](#running-the-application)
- [API Documentation](#api-documentation)
- [Testing](#testing)
- [Sample Data](#sample-data)
- [Screenshots](#screenshots)
- [Bonus Features](#bonus-features)
- [Troubleshooting](#troubleshooting)

## ✨ Features

### Core Features

- **Tab 1: Generate Quiz**
  - Input any Wikipedia article URL
  - Automatic content scraping using BeautifulSoup
  - AI-powered quiz generation (5-10 questions) using Google Gemini
  - Extract key entities (people, organizations, locations)
  - Display article sections
  - Generate related topics for further reading
  - Structured, card-based UI layout

- **Tab 2: Past Quizzes (History)**
  - View all previously generated quizzes
  - Sortable table with quiz details
  - Click "Details" to view full quiz in modal
  - Delete quizzes from history

### Quiz Features

- Multiple-choice questions (4 options each)
- Three difficulty levels: Easy, Medium, Hard
- Explanations for each answer
- Related Wikipedia topics suggestions

### Bonus Features Implemented ✅

- **Take Quiz Mode**: Interactive quiz with user scoring
- **URL Validation**: Validates Wikipedia URLs before processing
- **Caching**: Prevents duplicate scraping of the same URL
- **Error Handling**: Graceful handling of invalid URLs and network errors
- **Responsive Design**: Clean, minimal UI that works on all devices

## 🛠 Tech Stack

### Backend
- **Framework**: FastAPI 0.109.0
- **Database**: PostgreSQL (with SQLite fallback for development)
- **ORM**: SQLAlchemy 2.0.25
- **Web Scraping**: BeautifulSoup4 4.12.3
- **LLM Integration**: LangChain 0.1.6 + Google Gemini 1.5 Flash
- **Server**: Uvicorn

### Frontend
- **Framework**: React 18.2.0
- **Build Tool**: Vite 5.0.11
- **HTTP Client**: Axios 1.6.5
- **Icons**: Lucide React
- **Styling**: Custom CSS with CSS Variables

## 📁 Project Structure

```
Deepklarity/
├── backend/
│   ├── main.py                 # FastAPI application entry point
│   ├── models.py               # SQLAlchemy database models
│   ├── schemas.py              # Pydantic schemas for validation
│   ├── database.py             # Database connection configuration
│   ├── services/
│   │   ├── scraper.py          # Wikipedia scraping logic
│   │   └── llm_service.py      # LLM quiz generation service
│   ├── requirements.txt        # Python dependencies
│   ├── .env.example           # Environment variables template
│   └── .env                   # Your environment variables (create this)
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── GenerateQuiz.jsx    # Tab 1: Quiz generation
│   │   │   ├── QuizHistory.jsx     # Tab 2: History view
│   │   │   └── QuizDisplay.jsx     # Quiz display component
│   │   ├── api/
│   │   │   └── quiz.js             # API service layer
│   │   ├── App.jsx                 # Main app component
│   │   ├── App.css
│   │   ├── main.jsx
│   │   └── index.css
│   ├── package.json
│   ├── vite.config.js
│   └── index.html
├── sample_data/
│   ├── test_urls.md                # List of tested Wikipedia URLs
│   ├── alan_turing_quiz.json       # Sample output 1
│   ├── artificial_intelligence_quiz.json  # Sample output 2
│   └── langchain_prompts.md        # Prompt templates documentation
└── README.md
```

## 📋 Prerequisites

- **Python** 3.9 or higher
- **Node.js** 18 or higher
- **PostgreSQL** 14+ (or use SQLite for development)
- **Google API Key** for Gemini (free tier available)

## 🚀 Installation

### 1. Clone or Navigate to Project

```bash
cd "c:\Users\kunda\OneDrive\Desktop\Deepklarity"
```

### 2. Backend Setup

```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
# source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Frontend Setup

```bash
# Navigate to frontend directory
cd ..\frontend

# Install dependencies
npm install
```

## ⚙️ Configuration

### 1. Get Google Gemini API Key

1. Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Sign in with your Google account
3. Click "Create API Key"
4. Copy the generated API key

### 2. Configure Backend Environment

```bash
cd backend

# Copy example environment file
copy .env.example .env

# Edit .env file and add your API key
# GOOGLE_API_KEY=your_actual_api_key_here
```

**backend/.env** should contain:

```env
GOOGLE_API_KEY=your_google_api_key_here
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/wiki_quiz_db
# Or for SQLite (simpler for development):
# DATABASE_URL=sqlite:///./wiki_quiz.db
```

### 3. Database Setup

#### Option A: PostgreSQL (Recommended for Production)

```bash
# Install PostgreSQL and create database
# Then run:
createdb wiki_quiz_db

# Tables will be created automatically when you start the application
```

#### Option B: SQLite (Easier for Development)

Just use the SQLite URL in your .env file:
```env
DATABASE_URL=sqlite:///./wiki_quiz.db
```

No additional setup needed - the database file will be created automatically.

## 🏃 Running the Application

### Start Backend (Terminal 1)

```bash
cd backend
venv\Scripts\activate  # Activate virtual environment
python main.py
```

Backend will start at: `http://localhost:8000`

API docs available at: `http://localhost:8000/docs`

### Start Frontend (Terminal 2)

```bash
cd frontend
npm run dev
```

Frontend will start at: `http://localhost:3000`

### Access the Application

Open your browser and navigate to: **http://localhost:3000**

## 📚 API Documentation

### Base URL
```
http://localhost:8000
```

### Endpoints

#### 1. Generate Quiz
```http
POST /api/generate-quiz
Content-Type: application/json

{
  "url": "https://en.wikipedia.org/wiki/Alan_Turing",
  "force_regenerate": false
}
```

**Response:**
```json
{
  "id": 1,
  "url": "https://en.wikipedia.org/wiki/Alan_Turing",
  "title": "Alan Turing",
  "summary": "Alan Turing was a British mathematician...",
  "key_entities": {
    "people": ["Alan Turing", "Alonzo Church"],
    "organizations": ["University of Cambridge"],
    "locations": ["United Kingdom"]
  },
  "sections": ["Early life", "World War II", "Legacy"],
  "quiz": [
    {
      "question": "Where did Alan Turing study?",
      "options": ["Harvard", "Cambridge", "Oxford", "Princeton"],
      "answer": "Cambridge",
      "difficulty": "easy",
      "explanation": "Mentioned in the 'Early life' section."
    }
  ],
  "related_topics": ["Cryptography", "Enigma machine"],
  "created_at": "2026-02-14T10:30:00Z"
}
```

#### 2. Get All Quizzes
```http
GET /api/quizzes
```

#### 3. Get Quiz by ID
```http
GET /api/quizzes/{quiz_id}
```

#### 4. Delete Quiz
```http
DELETE /api/quizzes/{quiz_id}
```

### Interactive API Documentation

FastAPI provides automatic interactive documentation:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 🧪 Testing

### Manual Testing Steps

1. **Test Quiz Generation**
   ```
   1. Open http://localhost:3000
   2. Click "Generate Quiz" tab
   3. Enter: https://en.wikipedia.org/wiki/Alan_Turing
   4. Click "Generate Quiz" button
   5. Verify quiz appears with questions, options, and explanations
   ```

2. **Test Quiz History**
   ```
   1. Click "Past Quizzes" tab
   2. Verify previously generated quiz appears in table
   3. Click "View Details" icon
   4. Verify modal shows full quiz
   ```

3. **Test Take Quiz Mode**
   ```
   1. In any quiz view, click "Take Quiz" button
   2. Select answers for questions
   3. Click "Submit Quiz"
   4. Verify score is displayed
   ```

### Sample URLs to Test

See `sample_data/test_urls.md` for a comprehensive list:

- https://en.wikipedia.org/wiki/Alan_Turing
- https://en.wikipedia.org/wiki/Artificial_intelligence
- https://en.wikipedia.org/wiki/Albert_Einstein
- https://en.wikipedia.org/wiki/Python_(programming_language)
- https://en.wikipedia.org/wiki/World_War_II

### API Testing with cURL

```bash
# Generate quiz
curl -X POST http://localhost:8000/api/generate-quiz \
  -H "Content-Type: application/json" \
  -d "{\"url\": \"https://en.wikipedia.org/wiki/Alan_Turing\"}"

# Get all quizzes
curl http://localhost:8000/api/quizzes

# Get specific quiz
curl http://localhost:8000/api/quizzes/1
```

## 📊 Sample Data

The `sample_data/` folder contains:

1. **test_urls.md**: List of Wikipedia URLs tested with the application
2. **alan_turing_quiz.json**: Complete sample API output for Alan Turing article
3. **artificial_intelligence_quiz.json**: Sample output for AI article
4. **langchain_prompts.md**: Detailed documentation of LLM prompt templates

## 📸 Screenshots

### Tab 1: Generate Quiz
![Generate Quiz Interface](sample_data/screenshots/generate_quiz.png)
*Input Wikipedia URL and generate AI-powered quiz*

### Quiz Display with Questions
![Quiz Questions](sample_data/screenshots/quiz_display.png)
*Structured card layout showing questions with difficulty badges*

### Tab 2: Quiz History
![Quiz History Table](sample_data/screenshots/history_view.png)
*View all previously generated quizzes*

### Details Modal
![Quiz Details Modal](sample_data/screenshots/details_modal.png)
*Full quiz view in modal popup*

### Take Quiz Mode
![Take Quiz Mode](sample_data/screenshots/take_quiz.png)
*Interactive quiz mode with scoring*

## 🎁 Bonus Features

### ✅ Implemented

1. **Take Quiz Mode with User Scoring**
   - Hide answers until submission
   - Track user selections
   - Calculate and display score
   - Show correct/incorrect answers

2. **URL Validation and Preview**
   - Validates Wikipedia URL format
   - Shows article title after generation
   - Prevents invalid submissions

3. **Caching to Prevent Duplicate Scraping**
   - Checks database before scraping
   - Option to force regeneration
   - Significantly improves performance

4. **Comprehensive Error Handling**
   - Invalid URL detection
   - Network error recovery
   - Missing section handling
   - User-friendly error messages

5. **Section-wise Question Coverage**
   - Questions span multiple article sections
   - Explanations reference specific sections
   - Ensures comprehensive coverage

## 🔧 Troubleshooting

### Backend Issues

**Problem**: `ModuleNotFoundError: No module named 'fastapi'`
```bash
# Solution: Activate virtual environment and install dependencies
cd backend
venv\Scripts\activate
pip install -r requirements.txt
```

**Problem**: `google.api_core.exceptions.PermissionDenied`
```bash
# Solution: Check your Google API key in .env file
# Make sure GOOGLE_API_KEY is set correctly
```

**Problem**: Database connection error
```bash
# Solution: Use SQLite for development
# In backend/.env, set:
DATABASE_URL=sqlite:///./wiki_quiz.db
```

### Frontend Issues

**Problem**: `Cannot GET /api/generate-quiz`
```bash
# Solution: Make sure backend is running on port 8000
# Check vite.config.js proxy settings
```

**Problem**: CORS errors
```bash
# Solution: Already configured in main.py
# Make sure frontend runs on port 3000
```

### Common Issues

**Problem**: Quiz generation is slow
- This is normal - LLM processing takes 10-30 seconds
- Wait for the loading indicator to complete

**Problem**: No questions generated
- Check that Wikipedia URL is valid
- Ensure article has sufficient content
- Check backend logs for errors

## 📄 License

This project is created for educational purposes.

## 👨‍💻 Development

### Code Quality

- **Backend**: PEP 8 compliant, type hints, docstrings
- **Frontend**: ESLint configured, component-based architecture
- **Comments**: Meaningful comments explaining complex logic

### Key Design Patterns

1. **Service Layer**: Separation of business logic (scraper, LLM service)
2. **Repository Pattern**: Database access through SQLAlchemy ORM
3. **Component Composition**: Reusable React components
4. **API Service Layer**: Centralized API calls in frontend

## 🚀 Deployment

### Backend Deployment (e.g., Railway, Render)

1. Set environment variable `DATABASE_URL` to PostgreSQL connection string
2. Set `GOOGLE_API_KEY`
3. Deploy with: `uvicorn main:app --host 0.0.0.0 --port ${PORT}`

### Frontend Deployment (e.g., Vercel, Netlify)

1. Build: `npm run build`
2. Set environment variable `VITE_API_URL` to your backend URL
3. Deploy `dist/` folder

## 🤝 Contributing

For improvements or bug fixes:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📞 Support

For issues or questions:
- Check the Troubleshooting section
- Review sample data outputs
- Check API documentation at `/docs`

---

**Built with ❤️ using FastAPI, React, and Google Gemini AI**
