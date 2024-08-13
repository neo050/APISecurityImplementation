# app/__init__.py
import os
from flask import Flask
from flask.cli import load_dotenv

from routes import init_routes  # Use absolute import


def create_app():
    app = Flask(__name__)
    load_dotenv()
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

    # Initialize routes
    init_routes(app)

    return app
