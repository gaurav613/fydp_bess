from flask import Flask, render_template

app = Flask(__name__)

# @app.route("/")
# @app.route("/home")
# def home_page():
#     welcome_string = "Welcome to Batteryistic!"
#     return render_template('home.html', welcome=welcome_string)

@app.route("/")
@app.route("/home")
def home_page():
    welcome_string = "Welcome to Batteryistic!"
    dataframe = [
        {"MonthYear":"Jan 2021","CurrentBill": 12.00,"EstimatedPrice": 10.00, "Savings":2.00},
        {"MonthYear":"Feb 2021","CurrentBill": 13.00,"EstimatedPrice": 11.00, "Savings":3.00},
        {"MonthYear":"Mar 2021","CurrentBill": 14.00,"EstimatedPrice": 12.00, "Savings":4.00}
        ]
    return render_template('home.html', welcome=welcome_string, items=dataframe)

@app.route("/FAQ")
def FAQ_page():
    return render_template('FAQ.html')