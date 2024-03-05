from flask import Flask, request, jsonify, render_template, redirect, url_for
from flask_login import LoginManager, login_user, login_required, logout_user
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from AI.langchain import workout_query
from models.user_model import User
from extensions import db, login_manager


def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://rosanderg913:Titleist913!@localhost/workout_ai'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Recommended for production
    app.config['SECRET_KEY'] = 'RiPpErJoHnJoNeS'
    db.init_app(app)
    login_manager.init_app(app)
    with app.app_context():
        db.create_all()
    
    migrate = Migrate(app, db)

    return app

app = create_app()

@app.route('/workout', methods=['POST'])
def get_workout():
    data = request.get_json()
    muscle_group = data.get('muscle_group')
    training_style = data.get('training_style')
    rep_range = data.get('rep_range')

    if not all([muscle_group, training_style, rep_range]):
        return jsonify({"error": "Please provide all required fields."}), 400
    
    workout = workout_query(muscle_group, training_style, rep_range)


    return jsonify({'workout': workout.content})

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


