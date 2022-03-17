from app import app
from flask import jsonify, redirect, render_template, request, url_for, session, flash
from app.models import Item, User
from app.forms import RegisterForm, Tiered_Form, Timeofuse_Form

from datetime import timedelta
import datetime
from app import db
import pandas as pd
from app.forms import LOCATION_CHOICES
from datetime import timedelta
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
@app.route("/home", methods=['GET', 'POST'])
def home_page():
    return render_template('home.html')


@app.route("/FAQ")
def FAQ_page():
    return render_template('FAQ.html')


# @app.route("/output")
# def Output_page():
#     return render_template('output.html')
from plotly.subplots import make_subplots
import plotly.graph_objects as go
@app.route('/output')
def output_page():
    headers = ["Cost Graph", "GHG Graph"]
    descriptions = ["Plotting cost for each month", "Plotting GHG for each month"]
    fig = make_subplots(rows=2, cols=2)
    cost_rows = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
    cost_cols = [ 'Month', 'Act_cost','Est_cost','Cost_savings'] # Year	Month	Act_cost	Est_cost	Cost_savings
    cost_data = [[1, 179.63, 160.91, 18.72], [2, 170.63, 140.91, 18.72], [3, 189.63, 168.91, 18.72], [4, 199.63, 180.91, 18.72],[5, 178.63, 164.91, 18.72], [6, 188.63, 176.91, 18.72], [7, 180.63, 168.91, 18.72], [8, 175.63, 161.91, 18.72], [9, 170.63, 158.91, 18.72],[10, 168.63, 156.91, 18.72], [11, 190.63, 173.91, 18.72], [12, 159.63, 140.91, 18.72]]
    df_cost = pd.DataFrame(cost_data, index=cost_rows, columns=cost_cols)
    
    fig.append_trace(go.Scatter(
    x=df_cost['Month'],
    y=df_cost['Act_cost'],
    name="Original Cost"), row=1, col=1)
    fig.append_trace(go.Scatter(
    x=df_cost['Month'],
    y=df_cost['Est_cost'],
    name="BESST Cost"), row=1, col=1)
    fig.update_yaxes(title_text="Cost Savings", row=1, col=1)
    fig.update_xaxes(title_text="Month", row=1, col=1)

    fig.append_trace(go.Bar(
    x=df_cost['Month'],
    y=df_cost['Act_cost'],
    name="Original Cost"), row=1, col=2)
    fig.append_trace(go.Bar(
    x=df_cost['Month'],
    y=df_cost['Est_cost'],
    name="BESST Cost"), row=1, col=2)
    fig.update_yaxes(title_text="Cost Savings", row=1, col=2)
    fig.update_xaxes(title_text="Month", row=1, col=2)

    
    # df_cost = pd.read_csv("Data/costs.csv")
    # fig_cost = px.line(df_cost, x="Month", y="Cost")

    ghg_rows = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
    ghg_cols = ['Month', 'GHG']
    ghg_data = [[1, 15.488837], [2, 11.384587], [3, 16.468095], [4, 10.421837],[5, 15.653123], [6, 16.664116], [7, 19.721501], [8, 17.261196], [9, 14.567711],[10, 19.848164], [11, 18.907828], [12, 15.179477]]
    df_ghg = pd.DataFrame(ghg_data, index=ghg_rows, columns=ghg_cols)
    # df_ghg = pd.read_csv("Data/ghg.csv")
    # fig_ghg = px.line(ghg_cost, x="Month", y="GHG")
    fig.append_trace(go.Scatter(
    x=df_ghg['Month'],
    y=df_ghg['GHG'],
    name="GHG"), row=2, col=1)
    fig.update_yaxes(title_text="GHG Reduction", row=2, col=1)
    fig.update_xaxes(title_text="Month", row=2, col=1)

    fig.append_trace(go.Bar(
    x=df_ghg['Month'],
    y=df_ghg['GHG'],
    name="GHG"), row=2, col=2)
    fig.update_xaxes(title_text="Month", row=2, col=2)

    fig.update_layout(height=1500, width=1500, title_text="COST AND GHG GRAPHS")
    # fig = px.bar(df, x="Fruit", y="Amount", color="City", barmode="group")

    graphJSON_cost = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    # graphJSON_ghg = json.dumps(fig_ghg, cls=plotly.utils.PlotlyJSONEncoder) , graphJSON2= graphJSON_ghg
    return render_template('visualization.html', graphJSON1=graphJSON_cost, headers=headers,descriptions=descriptions)
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
            formDetails['Month_of_bill'] = form.Month_Of_bill.data.strftime("%m/%d/%Y")
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

            # formDetails['Tiered_Value'] = form.Tiered_Value.data
            # formDetails['Tiered_KWH'] = form.Tiered_KWH.data
            # formDetails['Tiered_Total'] = form.Tiered_Total.data
            formDetails['Month_of_bill'] = form.Month_Of_bill.data.strftime("%m/%d/%Y")
            formDetails['Location'] = dict(LOCATION_CHOICES).get(form.Location.data)
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


from .optimization_model import optimize
import json, ast


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
        dataReply = {'total': float(usage) * float(kwh)}
    else:
        dataReply = {'total': None}

    return jsonify(dataReply)



@app.route('/renderResults', methods=['GET', 'POST'])
def render_Results():
    complete_form = request.args['Complete_form']
    scrollto_results = request.args['scroll']
    # complete_form = complete_form.replace("'","\"").strip(" ")
    complete_form_dict = eval(complete_form) 
    # print(complete_form_dict)
    result = optimize(complete_form_dict)
    cost_savings = result[0]
    ghg_reduction = result[1]
    outage_reduction = result[2]
    ## plotting the results
    month_map = {1:"Jan", 2:"Feb", 3:"Mar", 4:"Apr", 5:"May", 6:"Jun", 7:"Jul", 8:"Aug", 9:"Sep", 10:"Oct", 11:"Nov", 12:"Dec"}

    cost_savings['Month_str'] = cost_savings['Month'].map(month_map)
    cost_savings['Date'] = cost_savings['Month_str'] + cost_savings['Year'].astype(str)

    ghg_reduction['Month_str'] = ghg_reduction['Month'].map(month_map)
    ghg_reduction['Date'] = ghg_reduction['Month_str'] + ghg_reduction['Year'].astype(str)
    fig = make_subplots(rows=3, cols=3)
    ### plotting cost comparison ###
    
    # scatter plot for original cost
    fig.append_trace(go.Scatter(
    x=cost_savings['Date'],
    y=cost_savings['Act_cost'],
    name="Original Cost"), row=1, col=1)
    # scatter plot for new cost
    fig.append_trace(go.Scatter(
    x=cost_savings['Date'],
    y=cost_savings['Est_cost'],
    name="BESST Cost"), row=1, col=1)

    fig.update_yaxes(title_text="Cost Savings", row=1, col=1)
    fig.update_xaxes(title_text="Month", row=1, col=1)

    # scatter plot for original cost
    fig.append_trace(go.Bar(
    x=cost_savings['Date'],
    y=cost_savings['Act_cost'],
    name="Original Cost"), row=1, col=2)
    # scatter plot for new cost
    fig.append_trace(go.Bar(
    x=cost_savings['Date'],
    y=cost_savings['Est_cost'],
    name="BESST Cost"), row=1, col=2)

    fig.update_yaxes(title_text="Cost Savings", row=1, col=2)
    fig.update_xaxes(title_text="Month", row=1, col=2)

    ### plotting GHG comparison ###
    # scatter plot for original ghg
    fig.append_trace(go.Scatter(
    x=ghg_reduction['Date'],
    y=ghg_reduction['Act_GHG'],
    name="Original GHG"), row=2, col=1)
    # scatter plot for new ghg
    fig.append_trace(go.Scatter(
    x=ghg_reduction['Date'],
    y=ghg_reduction['Est_GHG'],
    name="New GHG"), row=2, col=1)
    fig.update_yaxes(title_text="GHG Comparison", row=2, col=1)
    fig.update_xaxes(title_text="Date", row=2, col=1)

    # bar plot for original ghg
    fig.append_trace(go.Bar(
    x=ghg_reduction['Date'],
    y=ghg_reduction['Act_GHG'],
    name="Original GHG"), row=2, col=2)
    # bar plot for new ghg
    fig.append_trace(go.Bar(
    x=ghg_reduction['Date'],
    y=ghg_reduction['Est_GHG'],
    name="New GHG"), row=2, col=2)
    fig.update_xaxes(title_text="Date", row=2, col=2)

    ### plotting outage reduction ###
    # bar plot for new ghg
    fig.append_trace(go.Bar(
    x=outage_reduction['Period'],
    y=outage_reduction['Hours'],
    name="Hours", marker_color="firebrick"), row=3, col=1)
    fig.update_yaxes(title_text="Reliability - Hours Available", row=3, col=1)
    fig.update_xaxes(title_text="Peak periods", row=3, col=1)

    fig.update_layout(height=1800, width=1800, title_text="COST AND GHG GRAPHS")
    fig.update_layout(legend=dict(
    x=0.8
    ))
    # dataframe = result
    graphJSON_cost = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    # graphJSON_ghg = json.dumps(fig_ghg, cls=plotly.utils.PlotlyJSONEncoder) , graphJSON2= graphJSON_ghg
    return render_template('visualization.html', graphJSON1=graphJSON_cost)
    # DO THE MIP MODEL PROCESS HERE AND PASS IN THE RESULTS AS A PARAM
    # return render_template('home.html', savings=[dataframe], complete_form=complete_form, scrollto_results=scrollto_results)


