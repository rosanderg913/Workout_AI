from extensions import db

class Workout(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    muscle_group = db.Column(db.String(100), nullable=False)
    training_style = db.Column(db.String(100), nullable=False)
    rep_range = db.Column(db.String(100), nullable=False)
    plan = db.Column(db.Text, nullable=False)
    completed = db.Column(db.Boolean, default=False)
    notes = db.Column(db.Text, nullable=True)

    def __repr__(self):
        return f"<Workout {self.id}. Designed for {self.muscle_group}> using a {self.training_style} training style."
    