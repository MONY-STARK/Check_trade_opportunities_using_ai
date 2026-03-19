# 🏭 Trade Opportunities Analyzer

An AI-powered web application that analyzes **India's international trade sectors** and generates structured market opportunity reports using **Google Gemini**, **DuckDuckGo Search**, and **BeautifulSoup**.

---

## 📌 What It Does

You type a sector name like `pharmaceuticals` or `technology` — the app:

1. Searches the web for current news and market data about that sector in India
2. Scrapes the content from relevant pages
3. Sends all collected data to Google Gemini
4. Returns a detailed markdown report with trends, opportunities, risks, and recommendations

---

## 🖥️ Demo Flow

```
Register → Login → Enter Sector → Get Report → Download as .md
```

---

## 🚀 Features

- 🔐 **User Authentication** — Register and login with session management
- 🔍 **Live Web Search** — DuckDuckGo search for real-time sector data
- 🕸️ **Web Scraping** — BeautifulSoup extracts clean content from search results
- 🤖 **AI Analysis** — Google Gemini generates structured trade reports
- 📄 **Markdown Reports** — Download reports as `.md` files
- ⚡ **Rate Limiting** — Prevents API abuse per session
- 🛡️ **Input Validation** — Sanitizes all user inputs
- 💾 **In-Memory Storage** — No database required

---

## 📁 Project Structure

```
trade_opportunities/
│
├── app.py                  ← FastAPI application & routes
├── pipeline.py             ← Data collection + Gemini analysis
├── auth_data.py            ← Authentication logic
├── user_data.py            ← User session & data model
├── .env                    ← API keys 
├── requirements.txt        ← Python dependencies
│
└── templates/
    ├── index.html          ← Home page
    ├── login.html          ← Login page
    ├── register.html       ← Register page
    ├── app.html            ← Sector input page
    └── report.html         ← Report display page
```

---

## ⚙️ Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/MONY-STARK/Check_trade_opportunities_using_ai
cd Check_trade_opportunities_using_ai
```

### 2. Create a Virtual Environment

```bash
python -m venv venv

# On Linux/Mac
source venv/bin/activate

# On Windows
venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Get Your Gemini API Key

1. Go to [aistudio.google.com](https://aistudio.google.com)
2. Sign in with your Google account
3. Click **"Get API Key"**
4. Copy the key

### 5. Create `.env` File

Create a file called `.env` in the project root:

```
GEMINI_API_KEY=your_gemini_api_key_here
```

>

### 6. Run the App

```bash
uvicorn app:app --reload
```

### 7. Open in Browser

```
http://localhost:8000
```

---

## 📦 Requirements

```
fastapi
uvicorn
jinja2
python-multipart
requests
beautifulsoup4
lxml
ddgs
google-genai
python-dotenv
```

Install all at once:

```bash
pip install fastapi uvicorn jinja2 python-multipart requests beautifulsoup4 lxml ddgs google-genai python-dotenv
```

---

## 🔌 API Endpoints

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/` | Home page | ❌ |
| GET | `/register` | Register page | ❌ |
| POST | `/register` | Create account | ❌ |
| GET | `/login` | Login page | ❌ |
| POST | `/login` | Authenticate user | ❌ |
| POST | `/logout` | End session | ✅ |
| GET | `/app` | Sector input page | ✅ |
| GET | `/analyze?sector={}` | Generate report | ✅ |
| GET | `/download/{sector}` | Download `.md` file | ✅ |

---

## 📊 Sample Report Structure

When you analyze a sector, the report follows this structure:

```markdown
# Pharmaceuticals Sector — India Trade Opportunity Report

## Executive Summary
...

## Current Market Trends
- Trend 1 with numbers
- Trend 2 with numbers
...

## Trade Opportunities
### Opportunity 1: Generic Drug Exports
- Type: Export
- Market Size: $25 billion
- Target Markets: USA, Africa, UK
- Why Now: Patent cliffs creating demand
...

## Risks & Challenges
| Risk | Severity | How to Handle |
|------|----------|---------------|
...

## Government Policies & Support
...

## Recommendations
1. Short term (0-6 months): ...
2. Medium term (6-18 months): ...
3. Long term (18+ months): ...
```

---

## 🏗️ How The Pipeline Works

```
User enters sector name
        ↓
DuckDuckGo searched for latest news
        ↓
Top 5 URLs fetched and scraped with BeautifulSoup
        ↓
Clean text extracted from all pages
        ↓
Text + prompt sent to Google Gemini
        ↓
Gemini returns structured markdown report
        ↓
Report displayed in browser + downloadable as .md
```

---

## 🔒 Security Features

- **Session-based auth** — Cookie-based sessions with UUID tokens
- **Password verification** — Login checks credentials before access
- **Protected routes** — `/app`, `/analyze`, `/download` require valid session
- **Input sanitization** — Sector names validated before processing
- **Rate limiting** — Request count tracked per session
- **No hardcoded secrets** — All keys loaded from `.env`

---

## ⚠️ Known Limitations

- **In-memory storage** — All users and sessions are lost on server restart
- **Free tier limits** — Gemini free tier has quota limits (resets daily)
- **Scraping blocks** — Some websites may block the scraper; DuckDuckGo snippets used as fallback
- **No database** — By design, as per assignment requirements

---

## 🛠️ Troubleshooting

**Gemini 429 Error (Quota Exceeded)**
```
Wait 30 seconds and retry, or switch model name in pipeline.py
```

**Gemini 404 Error (Model Not Found)**
```python
# Run this to find available models for your key
for model in client.models.list():
    if "generateContent" in model.supported_actions:
        print(model.name)
```

**DuckDuckGo Not Returning Results**
```bash
pip install -U ddgs
```

**Templates Not Found**
```
Make sure you are running uvicorn from the project root directory
not from inside the templates folder
```

---

## 📄 License

MIT License — free to use and modify.

---

## 🙋 Author

Built as part of a backend engineering assignment.  
Stack: Python · FastAPI · Google Gemini · DuckDuckGo · BeautifulSoup
