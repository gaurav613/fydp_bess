from app import app
from flask import redirect, render_template, request, url_for, session, flash
from app.models import Item, User
from app.forms import RegisterForm, ElectricityInputForm
from datetime import timedelta
from app import db

app.permanent_session_lifetime = timedelta(seconds=10)

@app.route("/register", methods=["GET","POST"])
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

@app.route("/login", methods=["GET","POST"])
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
        return render_template('Profile.html', username = user)
    else:
        flash(f"Please log in to continue", "info")
        return redirect(url_for("login_page"))

@app.route("/", methods=['GET', 'POST'])
@app.route("/home",)
def home_page():
    return render_template('home.html')

@app.route("/FAQ")
def FAQ_page():
    return render_template('FAQ.html')

@app.route("/output")
def Output_page():
    return render_template('output.html')

@app.route('/renderInputs', methods=['GET', 'POST'])
def renderInputs():
    form = ElectricityInputForm()
    if form.validate_on_submit():
        flash(f"Running the model now!", "info")
        return redirect(url_for("renderInputs"))
    if form.errors != {}:
        for err_msg in form.errors.values():
            flash(f'Error in inputs: {err_msg}', category='danger')
    return render_template('home.html',  electricity_form = form)

# @app.route('/renderResults/', methods=['GET', 'POST'])
# def renderInputs():
#     dataframe = Item.query.all()
#     return render_template('home.html', savings=dataframe)
