import os
import json
import sys
from flask import request, jsonify
import google.generativeai as genai

# Add the current directory to the path so we can import utils if needed
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def get_question_count(word_count):
    """Determine number of questions based on document length"""
    if word_count < 500:
        return 5
    elif word_count < 1500:
        return 10
    elif word_count < 3000:
        return 15
    else:
        return 20

def main():
    """Main function for Vercel serverless function"""
    # Get JSON data
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No JSON data provided'}), 400

    text = data.get('text', '')
    difficulty = data.get('difficulty', 'medium')
    question_count = data.get('questionCount')

    # Validate input
    if not text or not text.strip():
        return jsonify({'error': 'No text provided'}), 400

    # Calculate question count if not provided
    if question_count is None:
        word_count = len(text.split())
        question_count = get_question_count(word_count)

    # Configure Gemini API
    api_key = os.environ.get('GEMINI_API_KEY')
    if not api_key:
        return jsonify({'error': 'Gemini API key not configured'}), 500

    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-1.5-flash')

    # Construct prompt
    prompt = f"""
You are an expert quiz generator. Based on the following text, generate {question_count} multiple-choice questions at {difficulty} difficulty level.

Text:
{text}

Requirements:
1. Each question must have exactly 4 options (A, B, C, D)
2. Only one option is correct
3. Provide a brief explanation for the correct answer
4. Format your response as a valid JSON array with exactly {question_count} objects
5. Each object must have these keys:
   - "question": string (the question text)
   - "options": array of exactly 4 strings (the answer choices)
   - "correct_index": integer (0-3 indicating the correct option)
   - "explanation": string (brief explanation of why the answer is correct)

Important: Return ONLY the JSON array. Do not include any additional text, markdown formatting, or explanations outside the JSON.

Example format:
[
  {{
    "question": "What is the capital of France?",
    "options": ["London", "Berlin", "Paris", "Madrid"],
    "correct_index": 2,
    "explanation": "Paris is the capital of France."
  }}
]
"""

    try:
        # Generate content with Gemini
        response = model.generate_content(prompt)

        # Extract JSON from response
        response_text = response.text.strip()

        # Try to find JSON array in the response
        # Look for content between [ and ]
        start_idx = response_text.find('[')
        end_idx = response_text.rfind(']')

        if start_idx == -1 or end_idx == -1:
            # If no brackets found, try to parse the whole response as JSON
            quiz_data = json.loads(response_text)
        else:
            json_str = response_text[start_idx:end_idx+1]
            quiz_data = json.loads(json_str)

        # Validate the structure
        if not isinstance(quiz_data, list):
            raise ValueError("Response is not a JSON array")

        if len(quiz_data) != question_count:
            # If we didn't get the expected number, we can still proceed with what we got
            pass

        # Validate each question
        for i, q in enumerate(quiz_data):
            if not all(key in q for key in ['question', 'options', 'correct_index', 'explanation']):
                raise ValueError(f"Question {i} missing required fields")
            if not isinstance(q['options'], list) or len(q['options']) != 4:
                raise ValueError(f"Question {i} must have exactly 4 options")
            if not isinstance(q['correct_index'], int) or q['correct_index'] < 0 or q['correct_index'] > 3:
                raise ValueError(f"Question {i} correct_index must be an integer between 0 and 3")

        return jsonify(quiz_data)

    except json.JSONDecodeError as e:
        # If JSON parsing fails, try again with a more explicit prompt
        try:
            fallback_prompt = prompt + "\n\nIMPORTANT: Your response must be ONLY a valid JSON array. No other text."
            response = model.generate_content(fallback_prompt)
            response_text = response.text.strip()

            # Try to extract JSON again
            start_idx = response_text.find('[')
            end_idx = response_text.rfind(']')
            if start_idx != -1 and end_idx != -1:
                json_str = response_text[start_idx:end_idx+1]
                quiz_data = json.loads(json_str)
                return jsonify(quiz_data)
            else:
                raise ValueError("Could not extract JSON from response")
        except Exception as fallback_error:
            return jsonify({'error': f'Failed to generate valid quiz after two attempts: {str(fallback_error)}'}), 500
    except Exception as e:
        return jsonify({'error': f'Failed to generate quiz: {str(e)}'}), 500

# For local testing with Vercel dev
if __name__ == '__main__':
    from flask import Flask
    app = Flask(__name__)

    @app.route('/api/generate-quiz', methods=['POST'])
    def generate_quiz():
        return main()

    app.run(debug=True)