from flask import session, Blueprint, jsonify, render_template, redirect, request, url_for, flash
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

# Route for creating a description
@app_views.route('/create', methods=['POST'])
def create_description():
    try:
        data = request.json  # Parse the JSON request data

        # Get the user_id from the session
        user_id = session.get('user_id')
        if not user_id:
            flash("You need to log in to access this page.")
            return redirect(url_for('app_views.login'))


        # Include the user_id in the payload sent to the orchestrator
        data['user_id'] = user_id

        # Forward the request to the orchestrator server
        orchestrator_response = requests.post(f"{ORCHESTRATOR_URL}/create", json=data)

        if orchestrator_response.status_code == 200:
            return orchestrator_response.json(), 200
        else:
            return jsonify({
                "error": "Failed to process the request via Orchestrator",
                "details": orchestrator_response.text
            }), orchestrator_response.status_code
    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500


@app_views.route('/translate', methods=['POST'])
def translate_description():
    try:
        data = request.json  # Parse the JSON request data

        # Get the user_id from the session
        user_id = session.get('user_id')
        if not user_id:
            flash("You need to log in to access this page.")
            return redirect(url_for('app_views.login'))

        # Include the user_id in the payload
        data['user_id'] = user_id

        # Forward the request to the orchestrator server
        orchestrator_response = requests.post(f"{ORCHESTRATOR_URL}/translate", json=data)

        if orchestrator_response.status_code == 200:
            return orchestrator_response.json(), 200
        else:
            return jsonify({
                "error": "Failed to process the translation via Orchestrator",
                "details": orchestrator_response.text
            }), orchestrator_response.status_code
    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500


@app_views.route('/enhance', methods=['POST'])
def enhance_description():
    try:
        data = request.json  # Parse the JSON request data

        # Get the user_id from the session
        user_id = session.get('user_id')
        if not user_id:
            flash("You need to log in to access this page.")
            return redirect(url_for('app_views.login'))

        # Include the user_id in the payload
        data['user_id'] = user_id

        # Forward the request to the orchestrator server
        orchestrator_response = requests.post(f"{ORCHESTRATOR_URL}/enhance", json=data)

        if orchestrator_response.status_code == 200:
            return orchestrator_response.json(), 200
        else:
            return jsonify({
                "error": "Failed to process the enhancement via Orchestrator",
                "details": orchestrator_response.text
            }), orchestrator_response.status_code
    except Exception as e:
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
                # Store user_id in session
                session['user_id'] = user_data.get('user_id')
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
            # Store user_id in session
            session['user_id'] = user_data.get('user_id')
            flash("Logged in successfully!")
            return redirect(url_for('app_views.account_create'))
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


@app_views.route('/account/history', methods=['GET'])
def history():
    try:
        # Check if the user is logged in
        user_id = session.get('user_id')
        if not user_id:
            flash("You need to log in to access the history.")
            return redirect(url_for('app_views.login'))

        # Fetch history data from orchestrator
        response = requests.get(f"{ORCHESTRATOR_URL}/history", params={"limit": 50, "user_id": user_id})
        if response.status_code == 200:
            history_data = response.json()
            return render_template('account/history.html', history=history_data)
        else:
            flash("Failed to fetch history from the server.")
            return render_template('account/history.html', history=[])
    except Exception as e:
        flash(f"An error occurred: {str(e)}")
        return render_template('account/history.html', history=[])


@app_views.route('/account/create', methods=['GET'])
def account_create():
    """
    Redirects the user to the create page or features page.
    """
    # Check if the user is logged in
    user_id = session.get('user_id')
    if not user_id:
        flash("You need to log in to access this page.")
        return redirect(url_for('app_views.login'))

    return render_template('account/create.html')


@app_views.route('/delete_record/<int:record_id>', methods=['POST'])
def delete_record(record_id):
    try:
        # Ensure the user is logged in
        user_id = session.get('user_id')
        if not user_id:
            flash("You need to log in to delete a record.")
            return redirect(url_for('app_views.login'))

        # Get the record type from the form data
        record_type = request.form.get('type')

        # Call the orchestrator to delete the record
        response = requests.post(
            f"{ORCHESTRATOR_URL}/delete_record/{record_id}",
            params={'type': record_type, 'user_id': user_id}
        )

        if response.status_code == 200:
            flash("Record deleted successfully.")
        else:
            flash("Failed to delete record. Please try again.")

        return redirect(url_for('app_views.history'))
    except Exception as e:
        flash(f"An error occurred: {str(e)}")
        return redirect(url_for('app_views.history'))


# @app_views.route('/clear_history', methods=['POST'])
# def clear_history():
#     try:
#         # Call the orchestrator's clear_records endpoint
#         response = requests.post(f"{ORCHESTRATOR_URL}/clear_records")

#         if response.status_code == 200:
#             flash("All records have been cleared successfully.")
#         else:
#             flash("Failed to clear records. Please try again.")

#         return redirect(url_for('app_views.history'))
#     except Exception as e:
#         flash(f"An error occurred: {str(e)}")
#         return redirect(url_for('app_views.history'))
