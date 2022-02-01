from enum import unique
from pickle import FALSE, TRUE
from app import db

class User(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(length=30), nullable=FALSE, unique=TRUE)
    email_address = db.Column(db.String(length=50), nullable=FALSE, unique=TRUE)
    password_hash = db.Column(db.String(length=60), nullable=FALSE)

class Item(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    Year = db.Column(db.String(length=4), nullable=False)
    Month = db.Column(db.String(length=10))
    CurrentBill = db.Column(db.Integer(), nullable=False)
    EstimatedPrice = db.Column(db.Integer(), nullable=False)
    Savings = db.Column(db.Integer(), nullable=False)

    def __repr__(self):
        return f'Item {self.Year}-{self.Month}'