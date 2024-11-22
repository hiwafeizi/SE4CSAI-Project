from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.dialects.postgresql import UUID
import uuid
from ..interface_server import db

class Users(db.Model):
    __tablename__ = 'users'

    # Use UUID as the primary key, generated automatically
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    email = db.Column(db.String(55), unique=True, nullable=True)

    # Security fields
    createdAt = db.Column(db.DateTime, default=datetime.utcnow)
    password_hash = db.Column(db.String(256))  # Stores hashed passwords
    role = db.Column(db.String(50), nullable=True, default='user')  # Optional field for role-based access control

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User {self.email} >'
