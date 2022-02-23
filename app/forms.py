from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField, FloatField, MonthField
from wtforms.validators import Length, EqualTo, Email, DataRequired, InputRequired,ValidationError
from app.models import User


class RegisterForm(FlaskForm):
    def validate_username(self, username_to_check):
        user = User.query.filter_by(username=username_to_check.data).first()
        if user:
            raise ValidationError("Username already exists! Please try a different username")

    def validate_email_address(self, email_address_to_check):
        email_address = User.query.filter_by(email_address=email_address_to_check.data).first()
        if email_address:
            raise ValidationError("Email address already exists! Please try a different email address")

    username= StringField(label='User Name', validators=[Length(min=2, max=30), DataRequired()])
    email_address = StringField(label='Email Address', validators=[Email(), DataRequired()])
    password1 = PasswordField(label='Password', validators=[Length(min=6), DataRequired()])
    password2 = PasswordField(label='Confirm Password', validators=[EqualTo("password1"), DataRequired()])
    submit = SubmitField(label='Create Account')

class ElectricityInputForm(FlaskForm):
    Bill_Type = SelectField(u'Type of electricity bill', choices=[('timeofuse', 'Time of Use'), ('tiered', 'Tiered')], validators=[DataRequired()])
    TimeofUse_Off_Peak_Value = FloatField(label='Off Peak', validators=[])
    TimeofUse_Off_Peak_KWH = FloatField(label='KWH', validators=[])
    TimeofUse_Off_Peak_Total = FloatField(label='Total', validators=[])
    TimeofUse_Mid_Peak_Value = FloatField(label='Mid Peak', validators=[])
    TimeofUse_Mid_Peak_KWH = FloatField(label='KWH', validators=[])
    TimeofUse_Mid_Peak_Total = FloatField(label='Total', validators=[])
    TimeofUse_On_Peak_Value = FloatField(label='On Peak', validators=[])
    TimeofUse_On_Peak_KWH = FloatField(label='KWH', validators=[])
    TimeofUse_On_Peak_Total = FloatField(label='Total', validators=[])

    Tiered_Value = StringField(label='Tiered Value', validators=[])
    Tiered_KWH = StringField(label='Tiered KWH', validators=[])
    Tiered_Total = FloatField(label='Tiered Total', validators=[])

    Month_Of_bill = MonthField(u'Month of bill', validators=[InputRequired()])
    DeliveryCharges =  FloatField(label='Delivery Charges', validators=[InputRequired()])
    RegulatoryCharges = FloatField(label='Regulatory Charges', validators=[InputRequired()])
    TotalElectricityCost = FloatField(label='Total Electricity Cost wo h.s.t', validators=[InputRequired()])

    submit = SubmitField(label='Next')

    