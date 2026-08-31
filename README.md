# QuizMate - Quiz Generator

QuizMate is a full-stack web application that helps students generate interactive quizzes from their course notes. Users can upload documents (text, PDF, or Word), select a difficulty level, and the app uses AI to generate multiple-choice questions. The quiz can be taken interactively in the browser, and users can download a PDF version with questions and answer key.

## Features

- **File Upload**: Accept .txt, .pdf, and .docx files (also allows pasting raw text directly)
- **AI-Powered Question Generation**: Uses Google Gemini API to generate quiz questions
- **Difficulty Selection**: Choose between Easy, Medium, and Hard difficulty levels
- **Automatic Question Count**: Determines optimal number of questions based on document length
- **Interactive Quiz UI**: Take the quiz in the browser with immediate feedback
- **Review Screen**: See your score, review each question with explanations
- **Downloadable PDF**: Generate a PDF containing questions and answer key
- **Responsive Design**: Works on mobile and desktop devices

## Tech Stack

- **Frontend**: HTML5, CSS3, Vanilla JavaScript (no frameworks)
- **Backend**: Python serverless functions (Vercel)
- **AI**: Google Gemini API (gemini-1.5-flash)
- **Dependencies**: PyPDF2, python-docx, reportlab, google-generativeai

## Setup Instructions

### Prerequisites

- Node.js and npm (for local development with Vercel)
- Python 3.8+
- A Google Gemini API key (free tier available at [Google AI Studio](https://aistudio.google.com/))

### Local Development

1. Clone the repository
2. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Create a `.env` file in the root directory with your Gemini API key:
   ```
   GEMINI_API_KEY=your_api_key_here
   ```
4. Start the Vercel development server:
   ```bash
   vercel dev
   ```
5. Open your browser to `http://localhost:3000`

### Deployment to Vercel

1. Push the code to a GitHub repository
2. Import the project in Vercel ([vercel.com](https://vercel.com))
3. Vercel will automatically detect the project structure and configure the build
4. Add your Gemini API key as an environment variable in Vercel's project settings:
   - Key: `GEMINI_API_KEY`
   - Value: `your_actual_api_key_here`
5. Deploy! Vercel will handle the rest.

## Project Structure

```
QuizMate/
├── public/
│   ├── index.html
│   ├── style.css
│   └── script.js
├── api/
│   ├── upload.py
│   ├── generate_quiz.py
│   └── generate_pdf.py
├── requirements.txt
├── README.md
├── .env.example
└── vercel.json
```

## Environment Variables

Create a `.env` file based on `.env.example`:

```
GEMINI_API_KEY=your_gemini_api_key_here
```

**Important**: Never commit your actual API key to version control. The `.env` file is listed in `.gitignore`.

## API Endpoints

All API endpoints are under `/api` and are implemented as Vercel serverless functions:

- `POST /api/upload` - Upload and extract text from files
- `POST /api/generate-quiz` - Generate quiz questions from text
- `POST /api/generate-pdf` - Generate PDF quiz with answer key

## How It Works

1. **Text Extraction**: The upload endpoint handles .txt, .pdf, and .docx files, extracting plain text
2. **Question Generation**: The generate-quiz endpoint sends the text and difficulty to Gemini AI, which returns structured JSON with questions, options, correct answers, and explanations
3. **Quiz Interaction**: The frontend displays one question at a time, tracks user answers, and shows a results screen
4. **PDF Generation**: The generate-pdf endpoint creates a professional PDF with questions and answer key using reportlab

## Limitations (Free Tier)

- Google Gemini API has rate limits on the free tier
- PDF generation uses reportlab which is free and open-source
- No persistent storage - all data is lost when the session ends or page is refreshed
- Maximum file size is limited by Vercel's serverless function constraints (typically 4.5MB)

## Future Enhancements

- User accounts to save quiz history
- Support for more file formats (PowerPoint, Google Docs)
- Different question types (true/false, fill-in-the-blank)
- Timed quiz mode
- Shareable quiz links
- Dark mode toggle

## License

This project is open source and available under the MIT License.

## Acknowledgments

- Google Gemini API for the AI question generation
- Vercel for the serverless hosting platform
- The open-source libraries used: PyPDF2, python-docx, reportlab