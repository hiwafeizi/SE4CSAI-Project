from uuid import UUID
from flask import Blueprint, render_template, redirect, request, url_for, flash, session
from werkzeug.security import generate_password_hash
from .models import Users
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

@app_views.route('/admin_page', methods=['GET', 'POST'])
@csrf.exempt
def test():
    print(0)
    return role_required("admin")(admin_page)()

@role_required("user")
@app_views.route('/my-account', methods=['GET'])
def my_account():
    
    return render_template('my-account.html')

@role_required("admin")  # Ensure only admins can access this
@csrf.exempt  # Exempt from CSRF only after role check
@app_views.route('/admin_page', methods=['GET', 'POST'])
def admin_page():
    VALID_ROLES = ['visitor', 'user', 'admin']  # Define valid roles
    print(session)
    
    if request.method == 'POST':
        # Handle the role update
        user_id = request.form.get('user_id')
        new_role = request.form.get('role')

        user_id = UUID(user_id)
        
        # Validate the role
        if new_role not in VALID_ROLES:
            flash('Invalid role selected.', 'danger')
            return redirect(url_for('app_views.admin_page'))

        # Find the user by ID
        user = Users.query.get(user_id)
        if not user:
            flash('User not found', 'danger')
            return redirect(url_for('app_views.admin_page'))

        # Update the role if valid
        try:
            user.role = new_role
            db.session.commit()  # Commit the change to the database
            flash(f'Role updated to {new_role} for user {user.email}', 'success')
        except Exception as e:
            db.session.rollback()  # Roll back in case of error
            flash('An error occurred while updating the role.', 'danger')
            print(f"Error: {e}")  # Log the error for debugging

        return redirect(url_for('app_views.admin_page'))
    
    # Handle the GET request: Fetch and display all users
    users = Users.query.all()
    return render_template('admin_page.html', users=users, valid_roles=VALID_ROLES)

@app_views.route('/terms-of-service', methods=['GET'])
def terms_of_service():
    return render_template('terms_of_service.html')

@app_views.route('/privacy-policy', methods=['GET'])
def privacy_policy():
    return render_template('privacy_policy.html')


