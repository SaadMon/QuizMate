import os
import sys
from flask import request, jsonify, make_response
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT

# Add the current directory to the path so we can import utils if needed
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def main():
    """Main function for Vercel serverless function"""
    # Get JSON data
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No JSON data provided'}), 400

    quiz_data = data.get('quizData', [])
    user_answers = data.get('userAnswers', [])

    if not quiz_data:
        return jsonify({'error': 'No quiz data provided'}), 400

    # Create PDF
    from io import BytesIO
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=72, leftMargin=72, topMargin=72, bottomMargin=18)

    # Container for the 'Flowable' objects
    elements = []

    # Define styles
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        spaceAfter=30,
        alignment=TA_CENTER
    )

    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=18,
        spaceAfter=12,
        textColor=colors.darkblue
    )

    normal_style = styles['Normal']
    normal_style.fontSize = 12
    normal_style.spaceAfter = 6

    # Add title
    elements.append(Paragraph("QuizMate Generated Quiz", title_style))
    elements.append(Spacer(1, 12))

    # Add quiz questions
    elements.append(Paragraph("Quiz Questions", heading_style))
    elements.append(Spacer(1, 12))

    for i, question in enumerate(quiz_data):
        # Question text
        elements.append(Paragraph(f"{i+1}. {question['question']}", normal_style))

        # Options
        options_data = []
        for j, option in enumerate(question['options']):
            option_letter = chr(65 + j)  # A, B, C, D
            options_data.append([f"{option_letter}.", option])

        # Create table for options
        options_table = Table(options_data, colWidths=[0.5*inch, 5*inch])
        options_table.setStyle(TableStyle([
            ('ALIGN', (0,0), (-1,-1), 'LEFT'),
            ('FONTNAME', (0,0), (-1,-1), 'Helvetica'),
            ('FONTSIZE', (0,0), (-1,-1), 10),
            ('BOTTOMPADDING', (0,0), (-1,-1), 6),
            ('TOPPADDING', (0,0), (-1,-1), 6),
        ]))

        elements.append(options_table)
        elements.append(Spacer(1, 12))

    # Add page break before answer key
    elements.append(PageBreak())

    # Add answer key
    elements.append(Paragraph("Answer Key", heading_style))
    elements.append(Spacer(1, 12))

    for i, question in enumerate(quiz_data):
        correct_option = question['options'][question['correct_index']]
        correct_letter = chr(65 + question['correct_index'])

        # Determine if user answered correctly (if user answers provided)
        user_answer_text = ""
        if user_answers and i < len(user_answers) and user_answers[i] is not None:
            user_option = question['options'][user_answers[i]]
            user_letter = chr(65 + user_answers[i])
            if user_answers[i] == question['correct_index']:
                user_answer_text = f" (Your answer: {user_letter}. {user_option} - CORRECT)"
            else:
                user_answer_text = f" (Your answer: {user_letter}. {user_option} - INCORRECT)"

        elements.append(Paragraph(
            f"{i+1}. {correct_letter}. {correct_option}{user_answer_text}",
            normal_style
        ))
        elements.append(Paragraph(f"   Explanation: {question['explanation']}", normal_style))
        elements.append(Spacer(1, 8))

    # Build PDF
    doc.build(elements)

    # Get the value of the BytesIO buffer and write it to the response
    buffer.seek(0)
    response = make_response(buffer.read())
    buffer.close()

    # Set headers for PDF download
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = 'attachment; filename=quizmate-quiz.pdf'

    return response

# For local testing with Vercel dev
if __name__ == '__main__':
    from flask import Flask
    app = Flask(__name__)

    @app.route('/api/generate-pdf', methods=['POST'])
    def generate_pdf():
        return main()

    app.run(debug=True)