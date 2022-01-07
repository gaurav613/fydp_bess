from app import db

class Item(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    Year = db.Column(db.String(length=4), nullable=False)
    Month = db.Column(db.String(length=10))
    CurrentBill = db.Column(db.Integer(), nullable=False)
    EstimatedPrice = db.Column(db.Integer(), nullable=False)
    Savings = db.Column(db.Integer(), nullable=False)

    def __repr__(self):
        return f'Item {self.Year}-{self.Month}'