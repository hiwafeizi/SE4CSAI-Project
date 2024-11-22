# config.py
import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your_default_secret_key'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///orchestrator.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    AI_SERVER_URL = os.environ.get('AI_SERVER_URL') or 'http://127.0.0.1:5001'
