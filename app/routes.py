from app import app
from flask import jsonify, redirect, render_template, request, url_for, session, flash
from app.models import Item, User
from app.forms import RegisterForm, Tiered_Form, Timeofuse_Form
from datetime import timedelta
from app import db

import pandas as pd
import json
import plotly
import plotly.express as px

app.permanent_session_lifetime = timedelta(seconds=10)


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
@app.route("/home",methods=['GET', 'POST'])
def home_page():
    return render_template('home.html')


@app.route("/FAQ")
def FAQ_page():
    return render_template('FAQ.html')


# @app.route("/output")
# def Output_page():
#     return render_template('output.html')
@app.route('/output')
def Output_page():
    headers = ["Cost Graph", "GHG Graph"]
    descriptions = ["Plotting cost for each month", "Plotting GHG for each month"]
    df_cost = pd.read_csv("Data/costs.csv")
    fig_cost = px.line(df_cost, x="Month", y="Cost")

    df_ghg = pd.read_csv("Data/ghg.csv")
    fig_ghg = px.line(df_ghg, x="Month", y="GHG")
    # fig = px.bar(df, x="Fruit", y="Amount", color="City", barmode="group")

    graphJSON_cost = json.dumps(fig_cost, cls=plotly.utils.PlotlyJSONEncoder)
    graphJSON_ghg = json.dumps(fig_ghg, cls=plotly.utils.PlotlyJSONEncoder)
    return render_template('visualization.html', graphJSON1=graphJSON_cost, graphJSON2= graphJSON_ghg, headers=headers,descriptions=descriptions)
# @app.route('/renderInputs', methods=['GET', 'POST'])
# def renderInputs():
#     form = ElectricityInputForm()
#     if form.validate_on_submit():
#         flash(f"Running the model now!", "info")
#         return redirect(url_for("renderInputs"))
#     if form.errors != {}:

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

    # if form.errors != {}:  # If any errors occure in the form, print them
    #     for err_msg in form.errors.values():
    #         flash(f'Error in inputs: {err_msg}', category='danger')

    # render the home.html page
    return render_template('home.html', scroll=scroll)


@app.route('/renderInputs2', methods=['GET', 'POST'])
def renderInputs2():
    scroll = request.args.get("scroll")
    billtype = request.args.get("billtype")
    form = None
    if billtype == "timeofuse":
        form = Timeofuse_Form()
        print("============INITIALIZED TIMEOFUSE FORM============")
        if form.validate_on_submit():
            formDetails = {}
            formDetails["BillType"] = "timeofuse"
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
        form = Tiered_Form()
        print("============INITIALIZED TIERED FORM============")
        if form.validate_on_submit():
            formDetails = {}
            formDetails["BillType"] = "tiered"
            formDetails['Tiered_Value'] = form.Tiered_Value.data
            formDetails['Tiered_KWH'] = form.Tiered_KWH.data
            formDetails['Tiered_Total'] = form.Tiered_Total.data
            formDetails['Month_of_bill'] = form.Month_Of_bill.data
            formDetails['DeliveryCharges'] = form.DeliveryCharges.data
            formDetails['RegulatoryCharges'] = form.RegulatoryCharges.data
            formDetails['TotalElectricityCost'] = form.TotalElectricityCost.data
            flash(f"Running model now for tiered!", "info")
            return redirect(url_for("render_Results", Complete_form=formDetails, scroll="scrollto_results"))

    if form.errors != {}:  # If any errors occure in the form, print them
        for err_msg in form.errors.values():
            flash(f'Error in inputs: {err_msg}', category='danger')

    return render_template('home.html', newelectricity_form=form, scroll=scroll, billtype=billtype)

@app.route('/renderResults', methods=['GET', 'POST'])
def render_Results():
    complete_form = request.args['Complete_form']
    scrollto_results = request.args['scroll']
    dataframe = None

    # DO THE MIP MODEL PROCESS HERE AND PASS IN THE RESULTS AS A PARAM
    return render_template('home.html', savings=dataframe, complete_form=complete_form, scrollto_results=scrollto_results)
