# app/__init__.py
import os
from flask import Flask
from flask.cli import load_dotenv
from .routes import init_routes  # Use absolute import

# Load environment variables from .env file
load_dotenv()


def create_app():
    app = Flask(__name__)

    # Set the SECRET_KEY from environment variables
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'default_secret_key')
    # Initialize routes
    init_routes(app)
    print(f"SECRET_KEY: {os.getenv('SECRET_KEY', 'default_secret_key')}")

    return app


# Testing the SECRET_KEY loading
