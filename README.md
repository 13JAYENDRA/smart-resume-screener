# 🎯 Smart Resume Screener
 ✨ Features

- 📄 **Resume Parsing**: Automatically extract structured data from PDF and TXT resumes
- 🤖 **AI-Powered Matching**: Semantic matching using free LLM APIs (Groq/Ollama)
- 📊 **Section-wise Scoring**: Get detailed scores for Skills, Experience, Education, Cultural Fit, and Leadership
- 💡 **Smart Recommendations**: AI-generated justifications, strengths, and gaps analysis
- 🎨 **Modern UI**: Clean, responsive web interface with real-time updates
- 🔍 **Advanced Filtering**: Filter candidates by minimum match score
- 📈 **Visual Analytics**: Score visualizations with charts and progress bars
- 🚀 **Fast & Lightweight**: Built with FastAPI for high performance



🛠️ Technology Stack

Backend
- FastAPI- Modern, fast web framework
- Python 3.8+ - Core programming language
- PyPDF2 - PDF text extraction
- Groq API - Free LLM integration (Llama 3.3 70B)
- Uvicorn - ASGI server

Frontend
- HTML5 - Structure
- Tailwind CSS - Styling
- Vanilla JavaScript - Interactivity
- Chart.js- Data visualization

LLM Options
- Groq (Recommended) - Free cloud API with Llama 3.3
- Ollama - Local LLM deployment
- Fallback - Rule-based scoring when LLM unavailable

## 🏗️ Project Architecture

```
┌─────────────┐         ┌──────────────┐         ┌─────────────┐
│             │         │              │         │             │
│  Frontend   │────────▶│   FastAPI    │────────▶│  Groq/LLM   │
│  (HTML/JS)  │         │   Backend    │         │     API     │
│             │◀────────│              │◀────────│             │
└─────────────┘         └──────────────┘         └─────────────┘
                               │
                               ▼
                        ┌──────────────┐
                        │   Resume     │
                        │   Parser     │
                        └──────────────┘
                               │
                               ▼
                        ┌──────────────┐
                        │  In-Memory   │
                        │   Database   │
                        └──────────────┘
```

### Data Flow
1. User uploads resume (PDF/TXT) + job description
2. Backend extracts structured data (name, email, skills, experience, education)
3. LLM analyzes resume vs job description
4. System calculates overall score + section-wise scores
5. AI generates justification, strengths, and gaps
6. Frontend displays results with visualizations

## 📦 Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)
- Modern web browser

### Step 1: Clone Repository
```bash
git clone https://github.com/yourusername/smart-resume-screener.git
cd smart-resume-screener
```

### Step 2: Create Virtual Environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Get Free Groq API Key
1. Visit [https://console.groq.com](https://console.groq.com)
2. Sign up for free account
3. Create API key
4. Copy the key (starts with `gsk_...`)

### Step 5: Configure API Key
Open `llm_matcher.py` and update:
```python
GROQ_API_KEY = "your_groq_api_key_here"  # Replace with your actual key
```

## ⚙️ Configuration

### LLM Configuration

#### Option 1: Groq (Recommended)
```python
# In llm_matcher.py
GROQ_API_KEY = "gsk_your_actual_key_here"
USE_OLLAMA = False
```

**Advantages:**
- ✅ Free tier: 30 requests/minute
- ✅ Very fast response times
- ✅ High-quality Llama 3.3 70B model
- ✅ No local setup required

#### Option 2: Ollama (Local)
```bash
# Install Ollama from https://ollama.com
ollama pull llama2

# In llm_matcher.py
USE_OLLAMA = True
```

**Advantages:**
- ✅ Completely free (unlimited requests)
- ✅ Works offline
- ✅ Privacy-focused (data stays local)

#### Option 3: Fallback (No LLM)
If no API key is set, the system automatically uses rule-based scoring.

### Port Configuration
Default: `http://localhost:8000`

To change port, edit `main.py`:
```python
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)  # Change port here
```

## 🚀 Usage

### Start the Application

**Step 1: Start Backend**
```bash
python main.py
```

Output:
```
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO:     Started server process
INFO:     Application startup complete.
```

**Step 2: Open Frontend**
- Double-click `index.html`, or
- Open in browser: `file:///path/to/index.html`

### Upload a Resume

1. **Enter Job Description**
   ```
   We are looking for a Senior Python Developer with 5+ years of experience.
   
   Required Skills:
   - Python, Django, FastAPI
   - React, JavaScript
   - PostgreSQL, MongoDB
   - AWS, Docker, Kubernetes
   - Team Leadership
   
   Responsibilities:
   - Build scalable REST APIs
   - Lead development team
   - Code reviews and mentorship
   ```

2. **Upload Resume File**
   - Click "Choose File"
   - Select PDF or TXT resume
   - Click "Process Resume with AI"

3. **View Results**
   - Overall match score (1-10)
   - Section-wise breakdown
   - AI-generated justification
   - Strengths and gaps
   - Visual charts

### Filter Candidates
- Use "Min Score" dropdown to filter
- Options: All (0+), Medium (5+), High (7+), Excellent (9+)
- Click "Refresh" to reload

### View Full Profile
- Click "View Details" on any candidate card
- See complete analysis with all sections
- View radar chart visualization

## 📚 API Documentation

### Base URL
```
http://localhost:8000
```

### Endpoints

#### 1. Health Check
```http
GET /
```

**Response:**
```json
{
  "message": "Smart Resume Screener API",
  "status": "running"
}
```

#### 2. Upload Resume
```http
POST /upload-resume
Content-Type: multipart/form-data
```

**Parameters:**
- `file` (File): Resume file (PDF or TXT)
- `job_description` (String): Job description text

**Response:**
```json
{
  "success": true,
  "candidate_id": 1,
  "match_score": 8.5,
  "section_scores": {
    "skills": 9.0,
    "experience": 8.5,
    "education": 8.8,
    "cultural_fit": 8.7,
    "leadership": 8.0
  },
  "justification": "Strong match with relevant experience...",
  "strengths": [
    "Excellent technical skills",
    "Strong leadership experience",
    "Good cultural fit"
  ],
  "gaps": [
    "Limited cloud experience",
    "Could improve documentation skills"
  ],
  "recommendation": "Highly recommend for interview...",
  "parsed_data": {
    "name": "John Doe",
    "email": "john@email.com",
    "phone": "1234567890",
    "skills": ["Python", "Django", "FastAPI"],
    "experience": [...],
    "education": [...]
  }
}
```

#### 3. Get All Candidates
```http
GET /candidates?min_score=7
```

**Query Parameters:**
- `min_score` (Float, Optional): Minimum match score filter (default: 0)

**Response:**
```json
{
  "candidates": [
    {
      "id": "1",
      "name": "John Doe",
      "email": "john@email.com",
      "match_score": 8.5,
      "section_scores": {...},
      "justification": "...",
      "uploaded_at": "2025-10-15T14:30:00"
    }
  ]
}
```

#### 4. Get Single Candidate
```http
GET /candidate/{candidate_id}
```

**Response:** Full candidate object with all details

#### 5. Delete Candidate
```http
DELETE /candidate/{candidate_id}
```

**Response:**
```json
{
  "success": true,
  "message": "Candidate deleted"
}
```

#### 6. Batch Upload
```http
POST /batch-upload
Content-Type: multipart/form-data
```

**Parameters:**
- `files[]` (Files): Multiple resume files
- `job_description` (String): Job description

**Response:**
```json
{
  "results": [
    {
      "filename": "resume1.pdf",
      "success": true,
      "score": 8.5
    },
    {
      "filename": "resume2.pdf",
      "success": true,
      "score": 7.2
    }
  ]
}
```

## 🤖 LLM Integration

### Prompt Template

The system uses a structured prompt for consistent results:

```python
prompt = f"""You are an expert HR recruiter with deep understanding of candidate evaluation.

**Job Description:**
{job_description}

**Candidate Profile:**
Name: {name}
Skills: {skills}
Experience: {experience}
Education: {education}

**Task:**
Provide section-wise scores (1-10 for each):
1. Skills Match Score
2. Experience Score
3. Education Score
4. Cultural Fit Score
5. Leadership Potential Score

Also provide:
- Overall Score (weighted average)
- Top 3 Strengths
- Top 3 Gaps
- Recommendation (Hire/Interview/Reject)

**Output Format:**
Overall Score: [number]
Skills Score: [number]
Experience Score: [number]
Education Score: [number]
Cultural Fit Score: [number]
Leadership Score: [number]
Strengths: [strength1], [strength2], [strength3]
Gaps: [gap1], [gap2], [gap3]
Recommendation: [Your detailed recommendation]
"""
```

### Response Parsing

The system intelligently parses LLM responses:
- Extracts numeric scores (1-10)
- Validates score ranges
- Parses comma-separated strengths/gaps
- Handles various response formats
- Provides fallback scoring

### Error Handling

If LLM fails, the system automatically:
1. Attempts retry
2. Falls back to rule-based scoring
3. Logs error for debugging
4. Returns valid response to user

## 📁 Project Structure

```
smart-resume-screener/
│
├── main.py                 # FastAPI application & API endpoints
├── resume_parser.py        # Resume parsing & data extraction
├── llm_matcher.py         # LLM integration & scoring logic
├── requirements.txt       # Python dependencies
├── index.html            # Frontend dashboard
│
├── test_resume.txt       # Sample resume for testing
├── README.md             # This file
│
└── venv/                 # Virtual environment (not in git)
```

### File Descriptions

#### `main.py`
- FastAPI application setup
- CORS configuration
- API endpoints definition
- Request/response handling
- In-memory database management

#### `resume_parser.py`
- PDF text extraction (PyPDF2)
- TXT file reading
- Regex-based data extraction
- Name, email, phone parsing
- Skills extraction (300+ keywords)
- Experience timeline parsing
- Education details extraction

#### `llm_matcher.py`
- Groq API integration
- Ollama local integration
- Prompt engineering
- Response parsing
- Fallback scoring logic
- Section-wise scoring calculation

#### `index.html`
- Responsive UI design
- Tailwind CSS styling
- Chart.js visualizations
- Real-time API calls
- Modal dialogs
- Animations and transitions

## 🧪 Testing

### Test with Sample Resume

Create `sample_resume.txt`:
```
JOHN DOE
Email: john.doe@email.com
Phone: +1-234-567-8900

PROFESSIONAL SUMMARY
Senior Python Developer with 6+ years of experience building scalable web applications.

SKILLS
Python, Django, FastAPI, React, JavaScript, PostgreSQL, MongoDB, 
AWS, Docker, Kubernetes, Git, Agile, Team Leadership

EXPERIENCE
Senior Python Developer | Tech Corp | 2020 - Present
- Led team of 5 developers
- Built REST APIs with FastAPI
- Deployed on AWS with Docker

Python Developer | StartupXYZ | 2018 - 2020
- Developed web applications with Django
- Integrated payment systems

EDUCATION
Bachelor of Computer Science | University | 2018
GPA: 3.8/4.0
```

### Test Job Description
```
Senior Python Developer needed with 5+ years experience.
Must have: Python, Django, FastAPI, React, AWS, Docker.
Leadership experience preferred.
```

### Expected Results
- Overall Score: 8-9/10
- Skills Score: 9/10
- Experience Score: 8.5/10
- High match probability

## 🐛 Troubleshooting

### Common Issues

#### Issue: "Module not found"
```bash
pip install -r requirements.txt
```

#### Issue: "CORS error" in browser
Check `main.py` has:
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

#### Issue: "Groq API error"
- Verify API key is correct in `llm_matcher.py`
- Check internet connection
- Verify free tier limits (30 req/min)

#### Issue: "PDF parsing error"
- Ensure PDF is not password-protected
- Try converting PDF to TXT
- Check PyPDF2 is installed

#### Issue: "Port 8000 already in use"
Change port in `main.py`:
```python
uvicorn.run(app, host="0.0.0.0", port=8001)
```

## 🔒 Security Notes

### Production Deployment

For production use, implement:

1. **Authentication**
   - Add user login/registration
   - JWT token-based auth
   - Role-based access control

2. **Database**
   - Replace in-memory storage
   - Use PostgreSQL/MongoDB
   - Implement data encryption

3. **API Security**
   - Rate limiting
   - API key validation
   - Input sanitization
   - HTTPS only

4. **File Validation**
   - Virus scanning
   - File size limits
   - Content validation
   - Sandboxed parsing

5. **Environment Variables**
   - Move API keys to `.env`
   - Use `python-dotenv`
   - Never commit secrets

## 🚀 Future Enhancements

### Planned Features
- [ ] Database integration (PostgreSQL)
- [ ] User authentication system
- [ ] Bulk resume processing (10+ files)
- [ ] Email notifications
- [ ] Advanced analytics dashboard
- [ ] Export to Excel/PDF
- [ ] Interview scheduling
- [ ] Resume templates
- [ ] Multi-language support
- [ ] Mobile app

### Advanced LLM Features
- [ ] Custom prompt templates
- [ ] Multi-model comparison
- [ ] Fine-tuned models
- [ ] Conversation history
- [ ] Explainable AI features
