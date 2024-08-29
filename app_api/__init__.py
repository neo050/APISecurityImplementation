# app/__init__.py

import os
from flask import Flask
from flask.cli import load_dotenv
from .routes import init_routes  # Use absolute import
from .config import config_by_name  # Import the config settings

# Load environment variables from .env file
load_dotenv()

def create_app():
    app = Flask(__name__)

    # Load the configuration from the 'prod' environment
    app.config.from_object(config_by_name['prod'])

    # Initialize routes
    init_routes(app)

    app.config['SECRET_KEY']

    return app
