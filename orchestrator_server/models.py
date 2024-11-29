from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), nullable=False, unique=True)
    password_hash = db.Column(db.String(256), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class PetDescriptionRequest(db.Model):
    __tablename__ = 'pet_description_requests'

    id = db.Column(db.Integer, primary_key=True)
    animal_type = db.Column(db.String(50), nullable=False)
    primary_breed = db.Column(db.String(50), nullable=False)
    gender = db.Column(db.String(10), nullable=False)
    primary_color = db.Column(db.String(50), nullable=False)
    maturity_size = db.Column(db.String(50), nullable=False)
    fur_length = db.Column(db.String(50), nullable=False)
    vaccinated = db.Column(db.String(10), nullable=False)
    dewormed = db.Column(db.String(10), nullable=False)
    sterilized = db.Column(db.String(10), nullable=False)
    health = db.Column(db.String(50), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    fee = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(20), default='pending')  # pending, processing, completed
    result = db.Column(db.Text, nullable=True)


class TranslationRequest(db.Model):
    __tablename__ = 'translation_requests'

    id = db.Column(db.Integer, primary_key=True)
    input_text = db.Column(db.Text, nullable=False)
    result_text = db.Column(db.Text, nullable=True)
    status = db.Column(db.String(20), default='pending')  # pending, processing, completed


class EnhancementRequest(db.Model):
    __tablename__ = 'enhancement_requests'

    id = db.Column(db.Integer, primary_key=True)
    input_text = db.Column(db.Text, nullable=False)
    result_text = db.Column(db.Text, nullable=True)
    status = db.Column(db.String(20), default='pending')  # pending, processing, completed
