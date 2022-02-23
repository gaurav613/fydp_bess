from flask import Flask
from flask_sqlalchemy import SQLAlchemy
# import config
import os

app = Flask(__name__)
app.config.from_object('config.ProdConfig')

db = SQLAlchemy(app)

from app import routes