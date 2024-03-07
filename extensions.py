from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import os

api_key = os.getenv('OPENAI_API_KEY')

db = SQLAlchemy()
login_manager = LoginManager()