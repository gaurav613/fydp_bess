from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL').replace("postgres://", "postgresql://", 1) 
app.config['SECRET_KEY'] = '803hfteyuse943h12'
db = SQLAlchemy(app)

from app import routes