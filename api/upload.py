import os
import sys
from flask import request, jsonify

# Add the current directory to the path so we can import utils if needed
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def extract_text_from_txt(file_stream):
    """Extract text from a .txt file"""
    try:
        # Read and decode the file
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

def main():
    """Main function for Vercel serverless function"""
    # Handle file upload
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400

    # Get file extension
    filename = file.filename.lower()
    if filename.endswith('.txt'):
        text = extract_text_from_txt(file.stream)
    elif filename.endswith('.pdf'):
        text = extract_text_from_pdf(file.stream)
    elif filename.endswith('.docx'):
        text = extract_text_from_docx(file.stream)
    else:
        return jsonify({'error': 'Unsupported file format. Please upload .txt, .pdf, or .docx'}), 400

    # Check if text is empty
    if not text or text.strip() == '':
        return jsonify({'error': 'The uploaded file appears to be empty'}), 400

    return jsonify({'text': text})

# For local testing with Vercel dev
if __name__ == '__main__':
    from flask import Flask
    app = Flask(__name__)

    @app.route('/api/upload', methods=['POST'])
    def upload():
        return main()

    app.run(debug=True)