from extensions import db
from datetime import datetime

class Workout(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    muscle_group = db.Column(db.String(100), nullable=False)
    training_style = db.Column(db.String(100), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    completed = db.Column(db.Boolean, default=False)
    notes = db.Column(db.Text, nullable=True)
    exercises = db.relationship('Exercise', backref='workout', lazy=True)

    def __repr__(self):
        return f"<Workout {self.id}. Designed for {self.muscle_group}> using a {self.training_style} training style."
    

class Exercise(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    workout_id = db.Column(db.Integer, db.ForeignKey('workout.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    sets = db.Column(db.Integer, nullable=False)
    reps = db.Column(db.String(20), nullable=False)
    rest = db.Column(db.String(40), nullable=False)

    def __repr__(self):
        return f"<Exercise {self.id}. {self.name} for {self.sets} sets of {self.reps} with {self.rest} rest."
    