from flask import Flask, request, jsonify, render_template, redirect, url_for
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from AI.langchain import workout_query
from models.user_model import User
from models.workout_model import Workout, Exercise
from functions.AI_Response_Parse import extract_exercise_data
from extensions import db, login_manager, api_key
from dotenv import load_dotenv
import os

api_key = os.getenv('OPENAI_API_KEY')


def create_app():
    load_dotenv()
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URI')
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Recommended for production
    db.init_app(app)
    login_manager.init_app(app)
    with app.app_context():
        db.create_all()
    
    migrate = Migrate(app, db)

    return app

app = create_app()

@app.route('/workout', methods=['POST'])
@login_required
def create_workout():
    data = request.get_json()
    muscle_group = data.get('muscle_group')
    training_style = data.get('training_style')
    rep_range = data.get('rep_range')

    if not all([muscle_group, training_style, rep_range]):
        return jsonify({"error": "Please provide all required fields."}), 400
    
    workout = workout_query(muscle_group, training_style, rep_range)

    if not workout:
        return jsonify({"error": "Unable to generate workout."}), 500
    
    # Access the current user's ID
    user_id = current_user.id

    new_workout = Workout(
        user_id=user_id,
        muscle_group=muscle_group,
        training_style=training_style
    )

    exercise_list = extract_exercise_data(workout.content)

    # Create Exercise objects and add to the new workout
    for exercise in exercise_list:
        new_exercise = Exercise(
            workout_id=new_workout.id,
            name=f"Exercise {exercise['exercise_number']}",
            sets=exercise['sets'],
            reps=exercise['reps'],
            rest=exercise['rest']
        )
        new_workout.exercises.append(new_exercise)

    db.session.add(new_workout)
    db.session.commit()
    
    return workout.content

@app.route('/form-template', methods=['GET'])
def form_template():
    return render_template('form.html')


# Login Functionalities
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

#   Okay! So i was able to get the /login route to finally retrieve the user (can verify with test print statementws)
#   However, refer to gemini, i need to add a 'is_active' attribute to user model
#   Update my db, then retry
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')

        user = User.query.filter_by(username=username).first()
        print(user)
        print(user.check_password(password))
        if user and user.check_password(password) and user.is_active():
            login_user(user, remember=True)
            return render_template('index.html')
        else:
            return jsonify({"error": "Invalid username or password."}), 401
    else:
        return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        data = request.get_json()
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')

        if not all([username, password, email]):
            return jsonify({"error": "Please provide username and password."}), 400

        user = User.query.filter_by(username=username).first()

        if user:
            return jsonify({"error": "Username already exists."}), 400

        new_user = User(username=username, email=email)
        print(new_user)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()

        return jsonify({"message": "User created successfully."}), 201
    
    return render_template('register.html')


if __name__ == '__main__':
    app.run(debug=True)


