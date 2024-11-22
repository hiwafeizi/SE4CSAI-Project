from flask import Flask, request, jsonify
import os
from utils import generate_description, translate_text, enhance_text

app = Flask(__name__)

# Load environment variables from .env if necessary
AI_PORT = int(os.getenv('AI_PORT', 5002))

@app.route('/create', methods=['POST'])
def create_description():
    try:
        data = request.json
        description = data.get('description', '')
        if not description:
            return jsonify({'error': 'Description is required.'}), 400

        # Call the AI logic to generate a description
        result = generate_description(description)
        return jsonify({'message': result}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/translate', methods=['POST'])
def translate():
    try:
        data = request.json
        text = data.get('text', '')
        if not text:
            return jsonify({'error': 'Text is required.'}), 400

        # Call the AI logic to translate the text
        result = translate_text(text)
        return jsonify({'message': result}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/enhance', methods=['POST'])
def enhance():
    try:
        data = request.json
        text = data.get('text', '')
        if not text:
            return jsonify({'error': 'Text is required.'}), 400

        # Call the AI logic to enhance the text
        result = enhance_text(text)
        return jsonify({'message': result}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=AI_PORT, debug=True)
