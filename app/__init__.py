from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///monthlysavings.db'
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
# 'postgres://muymcjjhlqceoq:70b88f65cea022003d4b058b8e0d9ef6803114e143d40d5732d10747ba7cbd7d@ec2-34-205-209-14.compute-1.amazonaws.com:5432/d8pk5gullavrpl'

db = SQLAlchemy(app)

from app import routes