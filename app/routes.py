from app import app
from flask import render_template, request
from app.models import Item
from app.forms import RegisterForm

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
    General_Bill_Questions = [
        'Does your monthly bill use Time-of-Use(TOU) or Tiered?',
        'Month of bill',
        'Delivery Charges',
        'Regulatory Charges',
        'Total Electricity Cost wo h.s.t',]
    TimeOfUse_Questions = [
        'KWH @',
        'Total',
        'Off-peak',
        'Mid-peak',
        'High-peak',
    ]
    Tiered_Questions = [
        'Number',
        'KWH @',
        'Total'
    ]
    return render_template('home.html', general_questions=General_Bill_Questions,timeofuse_questions=TimeOfUse_Questions, tiered_questions=Tiered_Questions )

# @app.route('/renderResults/', methods=['GET', 'POST'])
# def renderInputs():
#     dataframe = Item.query.all()
#     return render_template('home.html', savings=dataframe)
