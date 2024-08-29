# app/config.py

import os

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'your_default_secret_key')

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///development.db'

class ProductionConfig(Config):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL',
                                        'postgresql://<username>:<password>@api-security-db-new.clmsyeomixmt.eu-north-1.rds.amazonaws.com:5432/<dbname>')

config_by_name = dict(
    dev=DevelopmentConfig,
    prod=ProductionConfig
)
