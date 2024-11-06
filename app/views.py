from flask import Blueprint, render_template, redirect, request, url_for, flash, session
from werkzeug.security import generate_password_hash
from .forms import AccountSetupForm
from .models import ContactMessage, Posts, Users, Accounts, db
from .extensions import login_manager
from .admin import role_required
from . import csrf
from datetime import datetime, timedelta

app_views = Blueprint('app_views', __name__)


@app_views.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@app_views.route('/login', methods=['GET', 'POST'])
@csrf.exempt
def login():
    if request.method == 'POST':
        # Handle the POST request (login submission)
        email = request.form.get('email')
        password = request.form.get('password')

        # Fetch the user from the database
        user = Users.query.filter_by(email=email).first()

        # Check if the user exists
        if not user:
            flash('No account found with the provided email.', 'danger')
            return render_template('login.html', email=email)  # Pass the email back to the template

        # Check if the password is correct
        if not user.check_password(password):
            flash('Incorrect password, please try again.', 'danger')
            return render_template('login.html', email=email)  # Pass the email back to the template

        # If authentication is successful
        session['user_id'] = user.id
        session['user_role'] = user.role  # Store user role in the session
        
        flash('Logged in successfully!', 'success')
        return redirect(url_for('app_views.my_account'))

    # Handle the GET request (show the login form with optional email)
    email = request.args.get('email', '')  # Get email from query parameters if present
    return render_template('login.html', email=email)


@app_views.route('/terms-of-service', methods=['GET'])
def terms_of_service():
    return render_template('terms_of_service.html')

@app_views.route('/privacy-policy', methods=['GET'])
def privacy_policy():
    return render_template('privacy_policy.html')


