from datetime import datetime
from sqlalchemy import ForeignKey, UniqueConstraint
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.dialects.postgresql import ARRAY, JSONB, UUID
from sqlalchemy.orm import relationship
import uuid
from . import db

class Users(db.Model):
    __tablename__ = 'users'

    # Use UUID as the primary key, generated automatically
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False)
    urn = db.Column(db.String(100), nullable=True) 
    first_name = db.Column(db.String(55), nullable=True)  # First name from LinkedIn
    last_name = db.Column(db.String(55), nullable=True)   # Last name from LinkedIn
    name = db.Column(db.String(55), nullable=True)  # Full name from LinkedIn
    linkedin_email = db.Column(db.String(55), unique=True, nullable=True)
    email = db.Column(db.String(55), unique=True, nullable=True)
    profile_picture = db.Column(db.String(500), nullable=True)  # LinkedIn profile picture URL
    language = db.Column(db.String(20), nullable=True)  # Preferred language
    linkedin_token = db.Column(db.String(1000), nullable=True)  # LinkedIn access token stored securely

    # New fields for credits, plan, and expiration date
    post_credits = db.Column(db.Integer, default=0)  # Number of remaining post credits
    image_credits = db.Column(db.Integer, default=0)  # Number of remaining image credits
    plan_name = db.Column(db.String(50), nullable=True)  # Stores the plan name (e.g., 'Personal', 'Business', 'Marketer')
    expire_date = db.Column(db.DateTime, nullable=True)  # Expiration date for the current plan

    # Security fields
    createdAt = db.Column(db.DateTime, default=datetime.utcnow)
    password_hash = db.Column(db.String(256))  # Stores hashed passwords
    role = db.Column(db.String(50), nullable=True, default='user')  # Optional field for role-based access control

    # Relationship with Accounts model
    accounts = relationship('Accounts', back_populates='user')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User {self.first_name} {self.last_name}>'


class Accounts(db.Model):
    __tablename__ = 'accounts'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=False)
    urn = db.Column(db.String(100), nullable=True)
    account_name = db.Column(db.String(100), nullable=False)  # Account name, unique per user
    linkedin_token = db.Column(db.String(1000), nullable=True)  # LinkedIn access token stored securely
    company_id = db.Column(db.Integer, nullable=True)  # LinkedIn Company ID
    
    # Other fields in your model remain the same
    about_user = db.Column(db.Text, nullable=True)
    suggested_topics = db.Column(JSONB, nullable=True)
    selected_topics = db.Column(JSONB, nullable=True)
    subjects_by_topic = db.Column(JSONB, nullable=True)
    generating_subjects = db.Column(db.Boolean, default=False, nullable=True)
    ctas = db.Column(JSONB, nullable=True)
    target_audience = db.Column(ARRAY(db.String), nullable=True)
    tone = db.Column(db.String(200), nullable=True)
    time_zone = db.Column(db.String(50), nullable=True)
    post_times = db.Column(ARRAY(db.String), nullable=True)
    image_url = db.Column(db.String(400), nullable=True)

    # Relationship with Users
    user = db.relationship('Users', back_populates='accounts')
    posts = db.relationship('Posts', back_populates='account', cascade="all, delete-orphan")

    __table_args__ = (
        UniqueConstraint('user_id', 'account_name', name='uq_user_account_name'),
    )

    def __repr__(self):
        return f'<Account {self.account_name} (User: {self.user.name})>'


class Posts(db.Model):
    __tablename__ = 'posts'

    # Primary key for the posts
    id = db.Column(db.Integer, primary_key=True)

    # Foreign key linking to the accounts table
    account_id = db.Column(db.Integer, db.ForeignKey('accounts.id'), nullable=False, index=True)
    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey('users.id'), nullable=False, index=True)

    # Content-related fields
    content_type = db.Column(db.String(50), nullable=False)  # e.g., 'post', 'article', etc.
    image_requested = db.Column(db.Boolean, nullable=False, default=False)  # To track if image is requested
    subject = db.Column(db.String(255), nullable=True)  # Post subject
    topic = db.Column(JSONB, nullable=True)  # Topic of the post
    cta = db.Column(JSONB, nullable=True)  # Call to Action, stored as a JSON object (can store multiple CTAs)
    post_content = db.Column(db.Text, nullable=True)  # Actual post content

    # Time-related fields
    scheduled_time = db.Column(db.DateTime, nullable=True, index=True)  # Scheduled time for the post
    scheduled_utc_time = db.Column(db.DateTime, nullable=True)  # Scheduled time for the post
    created_time = db.Column(db.DateTime, default=datetime.utcnow)  # Time when the post was created

    status = db.Column(db.String(50), nullable=False, default="draft")  # e.g., "draft", "scheduled", "published"

    # Relationship to Account (Foreign Key)
    account = db.relationship('Accounts', back_populates='posts')

    def __repr__(self):
        return f'<Post {self.id} (Account: {self.account_id})>'


class ContactMessage(db.Model):
    __tablename__ = 'contact_messages'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    reason = db.Column(db.String(50), nullable=False)
    message = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<ContactMessage {self.name}>'
