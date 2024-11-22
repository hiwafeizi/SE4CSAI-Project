from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

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
