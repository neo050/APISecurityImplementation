# app/config.py

import os

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'your_default_secret_key')
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///development.db'

class ProductionConfig(Config):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL',
                                        'postgresql://<username>:<password>@api-security-db-new.clmsyeomixmt.eu-north-1.rds.amazonaws.com:5432/<dbname>')
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # Avoids SQLAlchemy overhead warning

config_by_name = dict(
    dev=DevelopmentConfig,
    prod=ProductionConfig
)
