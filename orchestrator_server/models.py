from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), nullable=False, unique=True)
    password_hash = db.Column(db.String(256), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class PetDescriptionRequest(db.Model):
    __tablename__ = 'pet_description_requests'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', name='fk_pet_description_user_id'), nullable=False)
    user = db.relationship('User', backref=db.backref('pet_requests', lazy=True))

    animal_type = db.Column(db.String(50), nullable=False)
    primary_breed = db.Column(db.String(50), nullable=True)
    gender = db.Column(db.String(10), nullable=True)
    primary_color = db.Column(db.String(50), nullable=True)
    maturity_size = db.Column(db.String(50), nullable=True)
    fur_length = db.Column(db.String(50), nullable=True)
    vaccinated = db.Column(db.String(10), nullable=True)
    dewormed = db.Column(db.String(10), nullable=True)
    sterilized = db.Column(db.String(10), nullable=True)
    health = db.Column(db.String(50), nullable=True)
    quantity = db.Column(db.Integer, nullable=True)
    fee = db.Column(db.Float, nullable=True)
    input_text = db.Column(db.Text, nullable=True)
    result_text = db.Column(db.Text, nullable=True)
    status = db.Column(db.String(20), default='pending')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class TranslationRequest(db.Model):
    __tablename__ = 'translation_requests'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', name='fk_translation_user_id'), nullable=False)
    user = db.relationship('User', backref=db.backref('translation_requests', lazy=True))

    input_text = db.Column(db.Text, nullable=False)
    result_text = db.Column(db.Text, nullable=True)
    status = db.Column(db.String(20), default='pending')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class EnhancementRequest(db.Model):
    __tablename__ = 'enhancement_requests'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', name='fk_enhancement_user_id'), nullable=False)
    user = db.relationship('User', backref=db.backref('enhancement_requests', lazy=True))

    input_text = db.Column(db.Text, nullable=False)
    result_text = db.Column(db.Text, nullable=True)
    status = db.Column(db.String(20), default='pending')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
