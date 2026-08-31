import os
import sys
from flask import Flask, request, jsonify

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Top-level Flask app — Vercel's Python runtime looks for this
app = Flask(__name__)

def extract_text_from_txt(file_stream):
    """Extract text from a .txt file"""
    try:
        content = file_stream.read()
        if isinstance(content, bytes):
            return content.decode('utf-8')
        return content
    except Exception as e:
        raise Exception(f"Error reading TXT file: {str(e)}")

def extract_text_from_pdf(file_stream):
    """Extract text from a .pdf file"""
    try:
        import PyPDF2
        pdf_reader = PyPDF2.PdfReader(file_stream)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text() + "\n"
        return text
    except Exception as e:
        raise Exception(f"Error reading PDF file: {str(e)}")

def extract_text_from_docx(file_stream):
    """Extract text from a .docx file"""
    try:
        import docx
        doc = docx.Document(file_stream)
        text = ""
        for paragraph in doc.paragraphs:
            text += paragraph.text + "\n"
        return text
    except Exception as e:
        raise Exception(f"Error reading DOCX file: {str(e)}")

@app.route('/api/upload', methods=['POST'])
def upload():
    """Handle file upload and extract text from txt/pdf/docx"""
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400

    filename = file.filename.lower()
    if filename.endswith('.txt'):
        text = extract_text_from_txt(file.stream)
    elif filename.endswith('.pdf'):
        text = extract_text_from_pdf(file.stream)
    elif filename.endswith('.docx'):
        text = extract_text_from_docx(file.stream)
    else:
        return jsonify({'error': 'Unsupported file format. Please upload .txt, .pdf, or .docx'}), 400

    if not text or text.strip() == '':
        return jsonify({'error': 'The uploaded file appears to be empty'}), 400

    return jsonify({'text': text})

# For local testing: `python api/upload.py`
if __name__ == '__main__':
    app.run(debug=True)