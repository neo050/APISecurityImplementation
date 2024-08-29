from flask import Flask
from flask.cli import load_dotenv
from flask_migrate import Migrate

from .config import config_by_name
from .models import db  # Import the database models
from .routes import init_routes  # Import the routes
import os

# Load environment variables from .env file
load_dotenv()

# Initialize SQLAlchemy and Migrate
migrate = Migrate()

def create_app():
    app = Flask(__name__)

    # Load configuration from config file
    app.config.from_object(config_by_name["prod"])

    # Set the SECRET_KEY from environment variables
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'default_secret_key')

    # Initialize SQLAlchemy
    db.init_app(app)

    # Initialize Migrate
    migrate.init_app(app, db)

    # Create the database tables
    with app.app_context():
        db.create_all()

    # Initialize routes
    init_routes(app)

    return app
