from flask import Blueprint, jsonify, render_template, redirect, request, url_for, flash
import requests
from flask_login import login_user, logout_user, current_user, login_required

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


@app_views.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        # Send data to the orchestrator for signup
        signup_response = requests.post(f"{ORCHESTRATOR_URL}/signup", json={"email": email, "password": password})
        
        if signup_response.status_code == 201:  # Successful signup
            # Automatically log in the user
            login_response = requests.post(f"{ORCHESTRATOR_URL}/login", json={"email": email, "password": password})
            
            if login_response.status_code == 200:  # Successful login
                user_data = login_response.json()
                # Handle session or flash messages if necessary
                flash("Signup and login successful!")
                return redirect(url_for('app_views.features'))
            else:
                flash("Signup successful, but login failed.")
                return redirect(url_for('app_views.login'))
        else:
            error_message = signup_response.json().get('error', 'Signup failed.')
            flash(error_message)
            return redirect(url_for('app_views.signup'))

    return render_template('signup.html')


@app_views.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        # Send data to the orchestrator for login
        response = requests.post(f"{ORCHESTRATOR_URL}/login", json={"email": email, "password": password})
        
        if response.status_code == 200:  # Successful login
            user_data = response.json()
            # handle user sessions here
            flash("Logged in successfully!")
            return redirect(url_for('app_views.features'))
        else:
            error_message = response.json().get('error', 'Login failed.')
            flash(error_message)
            return redirect(url_for('app_views.login'))

    return render_template('login.html')


@app_views.route('/logout', methods=['GET'])
@login_required
def logout():
    # Perform any session cleanup if necessary
    logout_user()
    flash("Logged out successfully!")
    return redirect(url_for('app_views.login'))
