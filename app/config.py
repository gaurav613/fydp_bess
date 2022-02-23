import os
import secrets

class Config:
    """Base config."""
    SECRET_KEY = secrets.token_urlsafe(16)
    STATIC_FOLDER = 'static'
    TEMPLATES_FOLDER = 'templates'

class ProdConfig(Config):
    FLASK_ENV = 'production'
    DEBUG = False
    TESTING = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL').replace("postgres://", "postgresql://", 1) 

class DevConfig(Config):
    FLASK_ENV = 'development'
    DEBUG = True
    TESTING = True
