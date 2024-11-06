from flask import session, flash, render_template
from functools import wraps

def role_required(required_roles, error_template='error_page.html'):
    def wrapper(func):
        @wraps(func)
        def decorated_view(*args, **kwargs):
            # Check if user is logged in and has a role
            if 'user_id' not in session or 'user_role' not in session:
                flash('You need to log in to access this page.', 'danger')
                return render_template(
                    error_template,
                    message='You need to log in to access this page.',
                    redirect_url='app_views.login'
                )

            # Check if the user has the required role
            user_role = session['user_role']
            if user_role not in required_roles:
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
