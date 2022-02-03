from app import app
from flask import render_template, request
from app.models import Item
from app.forms import RegisterForm, ElectricityInputForm

@app.route("/", methods=['GET', 'POST'])
@app.route("/home",)
def home_page():
    return render_template('home.html')

@app.route("/register")
def register_page():
    form = RegisterForm()
    return render_template('register.html', register_form=form)

@app.route("/FAQ")
def FAQ_page():
    return render_template('FAQ.html')

@app.route("/Profile/")
@app.route("/Profile/<username>")
def Profile_page(username=None):
    return render_template('Profile.html', username = username)

@app.route('/renderInputs', methods=['GET', 'POST'])
def renderInputs():
    form = ElectricityInputForm()
    return render_template('home.html',  electricity_form = form)

# @app.route('/renderResults/', methods=['GET', 'POST'])
# def renderInputs():
#     dataframe = Item.query.all()
#     return render_template('home.html', savings=dataframe)
