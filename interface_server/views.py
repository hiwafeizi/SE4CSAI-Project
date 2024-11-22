
from flask import Blueprint, render_template, redirect, request, url_for, flash, session
from werkzeug.security import generate_password_hash
from ..orchestrator_server.models import Users
from .extensions import login_manager
from .admin import role_required
from . import csrf, db

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
        
        flash('Logged in successfully!', 'success')
        return redirect(url_for('app_views.my_account'))

    return render_template('login.html')

@app_views.route('/signup', methods=['GET', 'POST'])
@csrf.exempt
def signup():
    if request.method == 'POST':
        # Get form data
        email = request.form.get('email')
        password = request.form.get('password')
        
        # Check if the email already exists
        existing_user = Users.query.filter_by(email=email).first()
        if existing_user:
            flash('An account with this email already exists.', 'danger')
            return render_template('signup.html', email=email)  # Pass the email back to the template

        # Hash the password for security
        hashed_password = generate_password_hash(password)

        # Create a new user instance
        new_user = Users(email=email, password_hash=hashed_password)

        # Save the new user to the database
        db.session.add(new_user)
        db.session.commit()

        # Log the new user in by setting the session variables
        session['user_id'] = new_user.id

        flash('Account created successfully! You are now logged in.', 'success')
        return redirect(url_for('app_views.my_account'))

    return render_template('signup.html')


@app_views.route('/terms-of-service', methods=['GET'])
def terms_of_service():
    return render_template('terms_of_service.html')

@app_views.route('/privacy-policy', methods=['GET'])
def privacy_policy():
    return render_template('privacy_policy.html')


