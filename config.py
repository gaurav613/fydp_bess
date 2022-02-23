import os
import secrets

is_prod = os.environ.get('IS_HEROKU', None)

class Config:
    SECRET_KEY = os.getenv(secrets.token_urlsafe(16), "this-is-the-default-key")
    STATIC_FOLDER = 'static'
    TEMPLATES_FOLDER = 'templates'

class ProdConfig(Config):
    if is_prod:
        SECRET_KEY = os.environ.get("SECRET_KEY")
        FLASK_ENV = 'production'
        DEBUG = False
        TESTING = False
        SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL').replace("postgres://", "postgresql://", 1)
    else:
        print("not_PROD")

