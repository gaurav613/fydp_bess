from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField

class RegisterForm(FlaskForm):
    username= StringField(label='User Name')
    email_address =  StringField(label='Email Address')
    password1 = PasswordField(label='Password')
    password2 = PasswordField(label='Confirm Password')
    submit = SubmitField(label='Create Account')

class ElectricityInputForm(FlaskForm):
    Bill_Type = SelectField(u'Does your monthly bill use Time-of-Use(TOU) or Tiered?', choices=[('timeofuse', 'Time of Use'), ('tiered', 'Tiered')])
    TimeofUse_Off_Peak_Value = StringField(label='TimeofUse_Off_Peak_Value')
    TimeofUse_Off_Peak_KWH = StringField(label='TimeofUse_Off_Peak_KWH')
    TimeofUse_Off_Peak_Total = StringField(label='TimeofUse_Off_Peak_Total')
    TimeofUse_Mid_Peak_Value = StringField(label='TimeofUse_Mid_Peak_Value')
    TimeofUse_Mid_Peak_KWH = StringField(label='TimeofUse_Mid_Peak_KWH')
    TimeofUse_Mid_Peak_Total = StringField(label='TimeofUse_Mid_Peak_Total')
    TimeofUse_On_Peak_Value = StringField(label='TimeofUse_On_Peak_Value')
    TimeofUse_On_Peak_KWH = StringField(label='TimeofUse_On_Peak_KWH')
    TimeofUse_On_Peak_Total = StringField(label='TimeofUse_On_Peak_Total')

    Tiered_Value = StringField(label='Tiered Value')
    Tiered_KWH = StringField(label='Tiered KWH')
    Tiered_Total = StringField(label='Tiered Total')

    Month_Of_bill = SelectField(u'Month of bill', choices=[('Time-Of-Use', 'Time of Use'), ('Tiered', 'Tiered')])
    DeliveryCharges =  StringField(label='Delivery Charges')
    RegulatoryCharges = StringField(label='Regulatory Charges')
    TotalElectricityCost = StringField(label='Total Electricity Cost wo h.s.t')

    submit = SubmitField(label='Next')