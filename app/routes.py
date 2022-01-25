from app import app
from flask import render_template
from app.models import Item

@app.route("/", methods=['GET', 'POST'])
@app.route("/home",)
def home_page():
    return render_template('home.html')

@app.route("/FAQ")
def FAQ_page():
    return render_template('FAQ.html')

@app.route("/Profile/")
@app.route("/Profile/<username>")
def Profile_page(username=None):
    return render_template('Profile.html', username = username)

@app.route('/renderSavings/', methods=['GET', 'POST'])
def renderSavings():
    dataframe = Item.query.all()
    return render_template('home.html', savings=dataframe)