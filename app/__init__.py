from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///monthlysavings.db' 
app.config['SECRET_KEY'] = "SOMERANDOMSTRING"

db = SQLAlchemy(app)

from app import routes
