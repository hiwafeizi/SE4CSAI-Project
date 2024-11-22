from flask import Flask
from flask_wtf.csrf import CSRFProtect
from dotenv import load_dotenv
import os
from datetime import timedelta

# Load environment variables from .env file
load_dotenv()

# Create Flask app
app = Flask(__name__)

# Configure app
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'default-secret-key')  # Add fallback for safety
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=300)  # Session expiration time

# Initialize CSRF protection
csrf = CSRFProtect(app)

# Register Blueprints
from views import app_views
app.register_blueprint(app_views)

if __name__ == '__main__':
    # Run the Flask app on a specific port
    app.run(host='0.0.0.0', port=5000, debug=True)
