<div align="center">

# 📚 QuizMate

### Turn any document into a quiz. Instantly.

<br>

## 🚀 [**▶ LAUNCH THE LIVE APP**](https://quiz-mate-beta.vercel.app/)
### 🔗 https://quiz-mate-beta.vercel.app/

*No install, no login — click the link above to test it right now.*

<br>

**Upload your notes → Pick a difficulty → Get a custom quiz → Study smarter.**

[![Made with Python](https://img.shields.io/badge/Backend-Python-3776AB?style=flat-square&logo=python&logoColor=white)](https://www.python.org/)
[![Powered by Gemini](https://img.shields.io/badge/AI-Google_Gemini-8E75B2?style=flat-square&logo=googlegemini&logoColor=white)](https://ai.google.dev/)
[![Deployed on Vercel](https://img.shields.io/badge/Deployed-Vercel-000000?style=flat-square&logo=vercel&logoColor=white)](https://vercel.com/)


[Features](#-features) · [How It Works](#-how-it-works) · [Setup](#-getting-started) · [Tech Stack](#-tech-stack)

</div>

---

## 💡 Why QuizMate?

Reading your notes over and over doesn't tell you what you actually *know*. Active recall does.

QuizMate takes any set of course notes — a PDF, a Word doc, or just pasted text — and turns it into a real, gradeable multiple-choice quiz in seconds. No manual question writing, no flashcard apps to configure. Upload, generate, test yourself.

Built as a self-directed project to explore full-stack development, AI integration, and serverless deployment — from a blank repo to a live, working product.

---

## ✨ Features

| | |
|---|---|
| 📄 **Multi-format upload** | Supports `.txt`, `.pdf`, and `.docx` — or just paste raw text |
| 🤖 **AI-generated questions** | Google Gemini analyzes your content and writes real multiple-choice questions |
| 🎚️ **Adjustable difficulty** | Easy, Medium, or Hard — tune how challenging the quiz feels |
| 🔢 **Smart question count** | Automatically scales the number of questions to your document's length |
| ✅ **Interactive quiz mode** | Answer questions right in the browser with instant, explained feedback |
| 📊 **Score + review screen** | See what you got right, what you missed, and why |
| ⬇️ **Downloadable PDF** | Export the full quiz + answer key for offline studying |
| 📱 **Responsive design** | Works cleanly on both desktop and mobile |

---

## 🖥️ How It Works

```
   📄 Upload Notes          🎯 Pick Difficulty         🤖 AI Generates          ✅ Take & Review
  (.txt / .pdf / .docx)   →   (Easy/Med/Hard)      →      Quiz              →     Your Quiz
```

1. **Upload** — Your file is parsed server-side and converted to plain text
2. **Generate** — The text + difficulty level is sent to Google's Gemini API, which returns structured quiz questions as JSON
3. **Practice** — Answer each question in a clean, distraction-free interface
4. **Review** — Get your score plus a full explanation for every answer
5. **Export** — Download a polished PDF version to study offline

---

## 🛠️ Tech Stack

<div align="center">

| Layer | Technology |
|---|---|
| **Frontend** | HTML5, CSS3, Vanilla JavaScript *(no frameworks — built from scratch)* |
| **Backend** | Python serverless functions |
| **AI Engine** | Google Gemini API *(free tier)* |
| **File Parsing** | PyPDF2, python-docx |
| **PDF Export** | ReportLab |
| **Hosting** | Vercel |

</div>

---

## 🚀 Getting Started

### Prerequisites
- Python 3.8+
- Node.js & npm *(for the Vercel CLI)*
- A free [Google Gemini API key](https://aistudio.google.com/)

### Run it locally

```bash
# 1. Clone the repo
git clone https://github.com/SaadMon/QuizMate.git
cd QuizMate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Add your API key
cp .env.example .env
# then open .env and paste your GEMINI_API_KEY

# 4. Launch the local dev server
vercel dev
```

Open **`http://localhost:3000`** and you're in.

### Deploy your own copy

1. Fork/push this repo to your own GitHub
2. Import it into [Vercel](https://vercel.com/new)
3. Add an environment variable: `GEMINI_API_KEY` → your key
4. Hit **Deploy** — that's it

---

## 📁 Project Structure

```
QuizMate/
├── public/              # Frontend
│   ├── index.html
│   ├── style.css
│   └── script.js
├── api/                 # Backend (Python serverless functions)
│   ├── upload.py         → parses .txt / .pdf / .docx
│   ├── generate_quiz.py  → calls Gemini, returns quiz JSON
│   └── generate_pdf.py   → builds downloadable PDF
├── requirements.txt
├── vercel.json
└── .env.example
```

---

## 🔮 Roadmap

- [ ] User accounts + quiz history
- [ ] Support for PowerPoint & Google Docs
- [ ] True/false & fill-in-the-blank question types
- [ ] Timed quiz mode
- [ ] Shareable quiz links
- [ ] Dark mode

---


<div align="center">

**Built by [Saad](https://github.com/SaadMon)**

⭐ If you found this useful, consider giving it a star!

</div>
