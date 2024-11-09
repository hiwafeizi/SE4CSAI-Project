from functools import wraps
from flask import flash, render_template, redirect, url_for, session
from app.models import Users

def role_required(required_roles, error_template='login.html'):
    # print("yesssss")
    def wrapper(func):
        @wraps(func)  
        def decorated_view(*args, **kwargs):
            # print(required_roles)
            # Check if user is logged in
            if 'user_id' not in session:
                flash('You need to log in to access this page.', 'danger')
                return render_template(
                    error_template,
                    message='You need to log in to access this page.',
                    redirect_url='app_views.login'
                )

            # Fetch the user from the database
            user_id = session['user_id']
            user = Users.query.get(user_id)
            if not user:
                flash('User not found. Please log in again.', 'danger')
                return redirect(url_for('app_views.login'))

            # Check if the user's role is one of the required roles
            if user.role not in required_roles:
                flash('You do not have permission to access this page.', 'danger')
                return render_template(
                    error_template,
                    message='You do not have permission to access this page.',
                    redirect_url='app_views.index'
                )

            # User is authorized, proceed with the original function
            return func(*args, **kwargs)
        return decorated_view
    return wrapper
