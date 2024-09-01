from flask import Flask
from flask.cli import load_dotenv
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.pool import QueuePool
from sqlalchemy.exc import OperationalError
from .config import config_by_name
from .models import db  # Import the database models
from .routes import init_routes  # Import the routes
import os
import time

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

    # Configure SQLAlchemy settings for connection pooling
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'postgresql+psycopg2://username:password@localhost/dbname')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
        'pool_size': 10,            # The size of the pool to be maintained, default is 5
        'max_overflow': 20,         # The maximum number of connections to allow in overflow, default is 10
        'pool_timeout': 30,         # The maximum number of seconds to wait before giving up on getting a connection from the pool
        'pool_recycle': 1800,       # Number of seconds after which a connection is automatically recycled
        'poolclass': QueuePool,     # The pool class to use
    }

    # Initialize SQLAlchemy with the configured app
    db.init_app(app)

    # Initialize Migrate
    migrate.init_app(app, db)

    # Create the database tables, with error handling and retry mechanism
    with app.app_context():
        retry_attempts = 5
        for attempt in range(retry_attempts):
            try:
                db.create_all()
                break
            except OperationalError as e:
                if attempt < retry_attempts - 1:
                    time.sleep(5)  # Wait 5 seconds before retrying
                else:
                    raise e

    # Initialize routes
    init_routes(app)

    return app
