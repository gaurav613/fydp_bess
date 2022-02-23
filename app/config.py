import os
import secrets

is_prod = os.environ.get('IS_HEROKU', None)

class Config:
    SECRET_KEY = secrets.token_urlsafe(16)
    STATIC_FOLDER = 'static'
    TEMPLATES_FOLDER = 'templates'

class ProdConfig(Config):
    if is_prod:
        FLASK_ENV = 'production'
        DEBUG = False
        TESTING = False
        SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL').replace("postgres://", "postgresql://", 1)
    else:
        print("not_PROD") 

class DevConfig(Config):
    FLASK_ENV = 'development'
    DEBUG = True
    TESTING = True
