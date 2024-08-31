import os

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'your_default_secret_key')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///development.db'

class ProductionConfig(Config):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'postgresql://postgres:.7tXS7#6Tsx5f,C@api-security-db.clmsyeomixmt.eu-north-1.rds.amazonaws.com:5432/postgres')

config_by_name = dict(
    dev=DevelopmentConfig,
    prod=ProductionConfig
)
