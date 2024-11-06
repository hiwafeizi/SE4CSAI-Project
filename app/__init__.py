from datetime import timedelta
import os
from flask import Blueprint, Flask
from .extensions import db, migrate, login_manager
from .models import Users
from flask_wtf.csrf import CSRFProtect
from dotenv import load_dotenv

csrf = None

def create_app():
    app = Flask(__name__)

    global csrf
    csrf = CSRFProtect(app)

    # Load environment variables from .env file
    load_dotenv()

    # Set the secret key from environment variable
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
    print("yoooo", os.environ.get('SECRET_KEY'))
    # Configuration setup for the database
    DATABASE_URI = os.environ.get('DATABASE_URL')

    # Use SQLite as a fallback if DATABASE_URL is not set
    if not DATABASE_URI:
        print("Warning: DATABASE_URL environment variable is not set. Using local SQLite database.")
        DATABASE_URI = "sqlite:///local_database.db"  # Set local SQLite database file path

    # Ensure correct database URI format for SQLAlchemy
    elif DATABASE_URI.startswith("postgres://"):
        DATABASE_URI = DATABASE_URI.replace("postgres://", "postgresql://", 1)
    
    app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URI
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)

    # Register Blueprints
    from .views import app_views
    app.register_blueprint(app_views)

    # User loader for Flask-Login
    @login_manager.user_loader
    def load_user(user_id):
        return Users.query.get(int(user_id))

    return app
