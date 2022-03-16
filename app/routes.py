from numpy import empty, number
from sqlalchemy import null, true
from app import app
from flask import jsonify, redirect, render_template, request, url_for, session, flash
from app.models import Item, User
from app.forms import RegisterForm, Tiered_Form, Timeofuse_Form
from datetime import date, timedelta
from app import db
import requests
import pandas as pd
from app.forms import LOCATION_CHOICES

# s = requests.session()
# app.permanent_session_lifetime = timedelta(seconds=10)


@app.route("/register", methods=["GET", "POST"])
def register_page():
    form = RegisterForm()
    if form.validate_on_submit():
        user_to_create = User(username=form.username.data,
                              email_address=form.email_address.data,
                              password_hash=form.password1.data)
        db.session.add(user_to_create)
        db.session.commit()
        flash(f"User created Sucessfully. Please log in to continue!", "info")
        return redirect(url_for("login_page"))
    if form.errors != {}:
        for err_msg in form.errors.values():
            flash(f'Error in user registration: {err_msg}', category='danger')
    return render_template('register.html', register_form=form)


@app.route("/login", methods=["GET", "POST"])
def login_page():
    if request.method == "POST":
        session.permanent = True
        user = request.form["username"]
        session["user"] = user
        flash(f"Logged in successfully as {user}", "info")
        return redirect(url_for("Profile_page"))
    else:
        if "user" in session:
            user = session["user"]
            flash(f"Already logged in as {user}", "info")
            return redirect(url_for("Profile_page"))
        else:
            return render_template("login.html")


@app.route("/logout",)
def logout():
    flash(f"Logged out successfully.", "info")
    session.pop("user", None)
    return redirect(url_for("login_page"))


@app.route("/user")
def Profile_page():
    if "user" in session:
        user = session["user"]
        return render_template('Profile.html', username=user)
    else:
        flash(f"Please log in to continue", "info")
        return redirect(url_for("login_page"))


@app.route("/", methods=['GET', 'POST'])
@app.route("/home", methods=['GET', 'POST'])
def home_page():
    return render_template('home.html')


@app.route("/FAQ")
def FAQ_page():
    return render_template('FAQ.html')


@app.route('/renderInputs1', methods=['GET', 'POST'])
def renderInputs1():
    scroll = request.args.get("scroll")

    if request.method == 'POST':
        if request.form.get('timeofuse') == 'Time of Use':

            print("timeofuse form reached")
            return redirect(url_for("renderInputs2", scroll="scrollto_electricity_form-inputs", billtype="timeofuse"))

        elif request.form.get('tiered') == 'Tiered':

            print("tiered form reached")
            return redirect(url_for("renderInputs2", scroll="scrollto_electricity_form-inputs", billtype="tiered"))
        else:
            pass

    elif request.method == 'GET':
        return render_template('home.html')

    # render the home.html page
    return render_template('home.html', scroll=scroll)


@app.route('/renderInputs2', methods=['GET', 'POST'])
def renderInputs2():
    scroll = request.args.get("scroll")
    billtype = request.args.get("billtype")
    form = None
    if billtype == "timeofuse":
        form = Timeofuse_Form(Location='9', csrf_enabled=False)
        print("============INITIALIZED TIMEOFUSE FORM============")
        if form.validate_on_submit():
            formDetails = {}
            formDetails["BillType"] = "timeofuse"
            formDetails['Location'] = dict(
                LOCATION_CHOICES).get(form.Location.data)
            formDetails['Off_Peak_Value'] = form.TimeofUse_Off_Peak_Value.data
            formDetails['Off_Peak_KWH'] = form.TimeofUse_Off_Peak_KWH.data
            formDetails['Off_Peak_Total'] = form.TimeofUse_Off_Peak_Total.data
            formDetails['Mid_Peak_Value'] = form.TimeofUse_Mid_Peak_Value.data
            formDetails['Mid_Peak_KWH'] = form.TimeofUse_Mid_Peak_KWH.data
            formDetails['Mid_Peak_Total'] = form.TimeofUse_Mid_Peak_Total.data
            formDetails['On_Peak_Value'] = form.TimeofUse_On_Peak_Value.data
            formDetails['On_Peak_KWH'] = form.TimeofUse_On_Peak_KWH.data
            formDetails['On_Peak_Total'] = form.TimeofUse_On_Peak_Total.data
            formDetails['Month_of_bill'] = form.Month_Of_bill.data
            formDetails['DeliveryCharges'] = form.DeliveryCharges.data
            formDetails['RegulatoryCharges'] = form.RegulatoryCharges.data
            formDetails['TotalElectricityCost'] = form.TotalElectricityCost.data
            flash(f"Running model now for timeofuse", "info")
            return redirect(url_for("render_Results", Complete_form=formDetails, scroll="scrollto_results"))
    if billtype == "tiered":
        form = Tiered_Form(Location='9', csrf_enabled=False)
        print("============INITIALIZED TIERED FORM============")
        if form.validate_on_submit():
            formDetails = {}
            formDetails["BillType"] = "tiered"
            formDetails['Location'] = dict(
                LOCATION_CHOICES).get(form.Location.data)
            formDetails['Tiered_LowerValue'] = form.Tiered_LowerValue.data
            formDetails['Tiered_LowerKWH'] = form.Tiered_LowerKWH.data
            formDetails['Tiered_LowerTotal'] = form.Tiered_LowerTotal.data
            formDetails['Tiered_UpperValue'] = form.Tiered_UpperValue.data
            formDetails['Tiered_UpperKWH'] = form.Tiered_UpperKWH.data
            formDetails['Tiered_UpperTotal'] = form.Tiered_UpperTotal.data
            formDetails['Month_of_bill'] = form.Month_Of_bill.data
            formDetails['DeliveryCharges'] = form.DeliveryCharges.data
            formDetails['RegulatoryCharges'] = form.RegulatoryCharges.data
            formDetails['TotalElectricityCost'] = form.TotalElectricityCost.data
            flash(f"Running model now for tiered!", "info")
            return redirect(url_for("render_Results", Complete_form=formDetails, scroll="scrollto_results"))

    if form.errors != {}:  # If any errors occure in the form, print them
        for key, value in form.errors.items():
            flash(f'{key} -> {value}', category='danger')

    return render_template('home.html', newelectricity_form=form, scroll=scroll, billtype=billtype)


@app.route('/get_autofill_inputKWH', methods=['GET', 'POST'])
def get_autofill_inputKWH():
    dataGet = request.get_json(force=True)
    d = dataGet['Date'].replace("-", ",")
    Historical_price = pd.read_csv(
        "https://raw.githubusercontent.com/gaurav613/fydp_bess/main/Data/Historical_price-byMonth.csv")
    row_ = Historical_price[Historical_price['Date'] == d]
    bill_type = dataGet['Bill_type']

    if bill_type == "timeofuse":
        if row_.empty:
            print("null found")
            dataReply = {
                'off': None,
                'mid': None,
                'on': None
            }
        else:
            dataReply = {
                'off': round(row_.iloc[0]['off_P']/100, 2),
                'mid': round(row_.iloc[0]['mid_P']/100, 2),
                'on': round(row_.iloc[0]['on_P']/100, 2)
            }
    if bill_type == "tiered":
        if row_.empty:
            print("null found")
            dataReply = {
                'off': None,
                'mid': None,
                'on': None
            }
        else:
            print("row found")
            dataReply = {
                'lower': round(row_.iloc[0]['lower_P']/100, 2),
                'upper': round(row_.iloc[0]['upper_P']/100, 2),
            }

    return jsonify(dataReply)


def is_float(str) -> bool:
    try:
        float(str)
        return True
    except ValueError:
        return False


@app.route('/get_autofill_inputTotal', methods=['GET', 'POST'])
def get_autofill_inputTotal():
    dataGet = request.get_json(force=True)
    usage = dataGet['usage']
    kwh = dataGet['kwh']

    if is_float(usage) == True and is_float(kwh) == True:
        dataReply = {'total': float(usage) + float(kwh)}
    else:
        dataReply = {'total': None}

    return jsonify(dataReply)


@app.route('/renderResults', methods=['GET', 'POST'])
def render_Results():
    complete_form = request.args['Complete_form']
    scrollto_results = request.args['scroll']
    dataframe = None

    # DO THE MIP MODEL PROCESS HERE AND PASS IN THE RESULTS AS A PARAM
    return render_template('home.html', savings=dataframe, complete_form=complete_form, scrollto_results=scrollto_results)
