from statistics import mean
from enum import auto
from turtle import bgcolor, color, width
from app import app
from statistics import mean
from app import db
from flask import jsonify, redirect, render_template, request, url_for, flash
from app.models import Item, User
from app.forms import RegisterForm, Tiered_Form, Timeofuse_Form
import datetime
from datetime import timedelta
import pandas as pd
from app.forms import LOCATION_CHOICES
from datetime import timedelta
import pandas as pd
import json
import plotly
from plotly.subplots import make_subplots
import plotly.graph_objects as go
from .optimization_model import optimize
import json

# @app.route("/register", methods=["GET", "POST"])
# def register_page():
#     form = RegisterForm()
#     if form.validate_on_submit():
#         user_to_create = User(username=form.username.data,
#                               email_address=form.email_address.data,
#                               password_hash=form.password1.data)
#         db.session.add(user_to_create)
#         db.session.commit()
#         flash(f"User created Sucessfully. Please log in to continue!", "info")
#         return redirect(url_for("login_page"))
#     if form.errors != {}:
#         for err_msg in form.errors.values():
#             flash(f'Error in user registration: {err_msg}', category='danger')
#     return render_template('register.html', register_form=form)


# @app.route("/login", methods=["GET", "POST"])
# def login_page():
#     if request.method == "POST":
#         session.permanent = True
#         user = request.form["username"]
#         session["user"] = user
#         flash(f"Logged in successfully as {user}", "info")
#         return redirect(url_for("Profile_page"))
#     else:
#         if "user" in session:
#             user = session["user"]
#             flash(f"Already logged in as {user}", "info")
#             return redirect(url_for("Profile_page"))
#         else:
#             return render_template("login.html")


# @app.route("/logout",)
# def logout():
#     flash(f"Logged out successfully.", "info")
#     session.pop("user", None)
#     return redirect(url_for("login_page"))


# @app.route("/user")
# def Profile_page():
#     if "user" in session:
#         user = session["user"]
#         return render_template('Profile.html', username=user)
#     else:
#         flash(f"Please log in to continue", "info")
#         return redirect(url_for("login_page"))


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
            formDetails['Month_of_bill'] = form.Month_Of_bill.data.strftime(
                "%m/%d/%Y")
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
            formDetails['Month_of_bill'] = form.Month_Of_bill.data.strftime(
                "%m/%d/%Y")
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
            dataReply = {
                'lower': None,
                'upper': None
            }
        else:
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
        dataReply = {'total': round(float(usage) * float(kwh), 2)}
    else:
        dataReply = {'total': None}

    return jsonify(dataReply)


@app.route('/renderResults/', methods=['GET', 'POST'])
def render_Results():
    complete_form = request.args['Complete_form']
    scrollto_results = request.args['scroll']

    complete_form_dict = eval(complete_form)
    result = optimize(complete_form_dict)
    cost_savings = result[0]
    ghg_reduction = result[1]
    outage_reduction = result[2]

    # plotting the results
    month_map = {1: "Jan", 2: "Feb", 3: "Mar", 4: "Apr", 5: "May", 6: "Jun",
                 7: "Jul", 8: "Aug", 9: "Sep", 10: "Oct", 11: "Nov", 12: "Dec"}

    cost_savings['Month_str'] = cost_savings['Month'].map(month_map)
    cost_savings['Date'] = cost_savings['Month_str'] + " " +\
        cost_savings['Year'].astype(str)

    ghg_reduction['Month_str'] = ghg_reduction['Month'].map(month_map)
    ghg_reduction['Date'] = ghg_reduction['Month_str'] + " " +\
        ghg_reduction['Year'].astype(str)

    ghg_reduction['Act_GHG'] = ghg_reduction['Act_GHG'].div(1000).round(2)
    ghg_reduction['Est_GHG'] = ghg_reduction['Est_GHG'].div(1000).round(2)
    outage_reduction['Hours'] = outage_reduction['Hours'].round(2)

    fig = make_subplots(rows=5, cols=1, vertical_spacing=0.1, subplot_titles=("Forcasted Annual Cost Savings",
                        "Forcasted Annual Cost Savings", "Monthly Greenhouse Gas Emissions",
                        "Monthly Greenhouse Gas Emissions", 
                        "Available Electricity During a Power Outage by Time-Of-Use Period"))

    ### plotting cost comparison ###
    # scatter plot for original cost
    trace1 = go.Scatter(
        x=cost_savings['Date'],
        y=cost_savings['Act_cost'],
        name="Estimated Cost WO Powerall")
    fig.append_trace(trace1, row=1, col=1)

    # scatter plot for new cost
    trace2 = go.Scatter(
        x=cost_savings['Date'],
        y=cost_savings['Est_cost'],
        name="Estimated Cost W Powerwall")
    fig.append_trace(trace2, row=1, col=1)
    fig.update_yaxes(title_text="Total Cost ($)", row=1, col=1)
    fig.update_xaxes(title_text="Month", row=1, col=1)

    # bar plot for original cost
    trace3 = go.Bar(
        x=cost_savings['Date'],
        y=cost_savings['Act_cost'],
        name="Estimated Cost WO Powerall")
    fig.append_trace(trace3, row=2, col=1)

    # bar plot for new cost
    trace4 = go.Bar(
        x=cost_savings['Date'],
        y=cost_savings['Est_cost'],
        name="Estimated Cost W Powerwall")
    fig.append_trace(trace4, row=2, col=1)
    fig.update_yaxes(title_text="Total Cost ($)", row=2, col=1)
    fig.update_xaxes(title_text="Month", row=2, col=1)

    ### plotting GHG comparison ###
    # scatter plot for original ghg
    trace5 = go.Scatter(
        x=ghg_reduction['Date'],
        y=ghg_reduction['Act_GHG'],
        name="Estimated GHG Emissions WO Powerall")
    fig.append_trace(trace5, row=3, col=1)
    # scatter plot for new ghg
    trace6 = go.Scatter(
        x=ghg_reduction['Date'],
        y=ghg_reduction['Est_GHG'],
        name="Estimated GHG Emissions W Powerwall")
    fig.append_trace(trace6, row=3, col=1)
    fig.update_yaxes(title_text="GHG Emissions (kgC02)", row=3, col=1)
    fig.update_xaxes(title_text="Month", row=3, col=1)

    # bar plot for original ghg
    trace7 = go.Bar(
        x=ghg_reduction['Date'],
        y=ghg_reduction['Act_GHG'],
        name="Estimated GHG Emissions WO Powerall")
    fig.append_trace(trace7, row=4, col=1)
    # bar plot for new ghg
    trace8 = go.Bar(
        x=ghg_reduction['Date'],
        y=ghg_reduction['Est_GHG'],
        name="Estimated GHG Emissions W Powerwall")
    fig.append_trace(trace8, row=4, col=1)
    fig.update_yaxes(title_text="GHG Emissions (kgC02)", row=4, col=1)
    fig.update_xaxes(title_text="Month", row=4, col=1)

    ### plotting outage reduction ###
    # bar plot for new ghg
    trace9 = go.Bar(
        x=outage_reduction['Period'],
        y=outage_reduction['Hours'],
        name="Hours of electricity available based on your usage in the period", marker_color="firebrick")
    fig.append_trace(trace9, row=5, col=1)
    fig.update_yaxes(title_text="Hours Available", row=5, col=1)
    fig.update_xaxes(title_text="Time-Of-Use Period", row=5, col=1)

    # calculate payback period
    yearly_savings = cost_savings.groupby('Year').sum()
    yearly_mean_savings = mean(yearly_savings['Cost_savings'])
    payback_period = round(10000/yearly_mean_savings, 1)

    # calculating ghg savings equivalent: smartphones charged - https://www.epa.gov/energy/greenhouse-gas-equivalencies-calculator
    # 1 kWh/charge x 1,562.4 pounds CO2/MWh delivered electricity x 1 metric ton/2,204.6 lbs
    total_ghg_saved = sum(ghg_reduction['GHG_red'])
    # phones charged from savings
    phones_charged_1_year = total_ghg_saved/8.22
    phones_charged_10_years = int(round(phones_charged_1_year, 0))
    # print(f'ghg {total_ghg_saved}\nphones 1 {phones_charged_1_year}\nphones 10 {phones_charged_10_years}')

    # miles driven
    miles_driven = round(total_ghg_saved/398)
    # fig.update_traces(hovertemplate=None, hoverlabel= {namelength :-1})
    fig.update_layout(
        hovermode="x unified",
        hoverlabel=dict(font_color='black', bgcolor='white', align='left',
                        bordercolor='white'),  # whatever format you want)
        autosize=True,
        showlegend=False,
        hoverlabel_namelength=-1,
        plot_bgcolor="#fafafa",
        margin=dict(l=10, r=35, t=60, b=10, pad=0),
        font=dict(
            size=12)
    )

    fig.update_layout(height=2650)
    fig.update_yaxes(automargin=True)

    for i in fig['layout']['annotations']:
        i['font'] = dict(size=15, color='black')

    graphJSON_cost = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

    return render_template('home.html', graphJSON1=graphJSON_cost, payback=payback_period, phonescharged_10=phones_charged_10_years, milesdriven=miles_driven, scrollto_results=scrollto_results)
