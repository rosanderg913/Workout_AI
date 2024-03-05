from werkzeug.security import generate_password_hash, check_password_hash
from .workout_model import Workout
from datetime import datetime

from extensions import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False, unique=True)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password_hash = db.Column(db.String(512))
    registered_on = db.Column(db.DateTime, default=datetime.utcnow)


    # Relationship with Workout model (one-to-many)
    workouts = db.relationship('Workout', backref='user', lazy='dynamic')

    def __repr__(self):
        return f"<User {self.username}>"
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)   
    
    # This is a required update for user model after switching from sqlite to mysql db
    def is_active(self):
        # You can define your own logic here to check if the user is active.
        # For example, you could check if the account is verified or not expired.
        return True  # For now, assume all users are active
    
    def get_id(self):
        """Returns the user's unique identifier."""
        return self.id  # Assuming 'id' is your primary key attribute
    
