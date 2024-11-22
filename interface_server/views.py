from flask import Blueprint, jsonify, render_template, redirect, request, url_for, flash
import requests

app_views = Blueprint('app_views', __name__)

ORCHESTRATOR_URL = "http://127.0.0.1:5001"  # Orchestrator server URL

@app_views.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app_views.route('/terms-of-service', methods=['GET'])
def terms_of_service():
    return render_template('terms_of_service.html')

@app_views.route('/privacy-policy', methods=['GET'])
def privacy_policy():
    return render_template('privacy_policy.html')

@app_views.route('/features', methods=['GET'])
def features():
    return render_template('features.html') 

@app_views.route('/create', methods=['POST'])
def create_description():
    try:
        data = request.json  # Parse the JSON request data

        # Forward the request to the orchestrator server
        orchestrator_response = requests.post(f"{ORCHESTRATOR_URL}/create", json=data)

        if orchestrator_response.status_code == 200:
            # Successfully processed by the orchestrator
            return orchestrator_response.json(), 200
        else:
            # Error in processing by the orchestrator
            return jsonify({
                "error": "Failed to process the request via Orchestrator",
                "details": orchestrator_response.result
            }), orchestrator_response.status_code
    except Exception as e:
        # Handle unexpected errors
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500


# Route for "Translate Descriptions"
@app_views.route('/translate', methods=['POST'])
def translate_description():
    try:
        data = request.json  # Parse the JSON request data

        # Validate input
        description = data.get('translate_input')
        if not description:
            return jsonify({'error': 'The translate_input field is required.'}), 400

        # Forward the request to the orchestrator server
        orchestrator_response = requests.post(f"{ORCHESTRATOR_URL}/translate", json={"translate_input": description})

        if orchestrator_response.status_code == 200:
            # Successfully processed by the orchestrator
            return orchestrator_response.json(), 200
        else:
            # Error in processing by the orchestrator
            return jsonify({
                "error": "Failed to process the translation via Orchestrator",
                "details": orchestrator_response.text
            }), orchestrator_response.status_code
    except Exception as e:
        # Handle unexpected errors
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500


# Route for "Enhance Descriptions"
@app_views.route('/enhance', methods=['POST'])
def enhance_description():
    try:
        data = request.json  # Parse the JSON request data

        # Validate input
        description = data.get('enhance_input')
        if not description:
            return jsonify({'error': 'The enhance_input field is required.'}), 400

        # Forward the request to the orchestrator server
        orchestrator_response = requests.post(f"{ORCHESTRATOR_URL}/enhance", json={"enhance_input": description})

        if orchestrator_response.status_code == 200:
            # Successfully processed by the orchestrator
            return orchestrator_response.json(), 200
        else:
            # Error in processing by the orchestrator
            return jsonify({
                "error": "Failed to process the enhancement via Orchestrator",
                "details": orchestrator_response.text
            }), orchestrator_response.status_code
    except Exception as e:
        # Handle unexpected errors
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500
