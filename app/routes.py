from app import app
from flask import render_template
from app.models import Item

@app.route("/")
@app.route("/home")
def home_page():
    dataframe = Item.query.all()
    return render_template('home.html', items=dataframe)

@app.route("/FAQ")
def FAQ_page():
    return render_template('FAQ.html')

@app.route("/Profile")
def Profile_page():
    return render_template('Profile.html')