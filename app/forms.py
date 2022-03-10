import datetime
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, FloatField, MonthField
from wtforms.validators import Length, EqualTo, Email, DataRequired, InputRequired, ValidationError, NumberRange
from app.models import User


class RegisterForm(FlaskForm):
    def validate_username(self, username_to_check):
        user = User.query.filter_by(username=username_to_check.data).first()
        if user:
            raise ValidationError(
                "Username already exists! Please try a different username")

    def validate_email_address(self, email_address_to_check):
        email_address = User.query.filter_by(
            email_address=email_address_to_check.data).first()
        if email_address:
            raise ValidationError(
                "Email address already exists! Please try a different email address")

    username = StringField(label='User Name', validators=[Length(min=2, max=30), DataRequired()])
    email_address = StringField(label='Email Address', validators=[Email(), DataRequired()])
    password1 = PasswordField(label='Password', validators=[Length(min=6), DataRequired()])
    password2 = PasswordField(label='Confirm Password', validators=[EqualTo("password1"), DataRequired()])
    submit = SubmitField(label='Create Account')

class Tiered_Form(FlaskForm):

    def validate_Month_Of_bill(self, Month_Of_bill):
        if Month_Of_bill.data < datetime.date(2015,4,1):
            raise ValidationError(
                "Please use a more recent bill!"
            )

    Month_Of_bill = MonthField(u'Month of bill', validators=[InputRequired()])
    Tiered_Value = FloatField(label='Tiered Value', validators=[InputRequired(), NumberRange(min=0,max=99999)])
    Tiered_KWH = FloatField(label='Tiered KWH', validators=[InputRequired(), NumberRange(min=0,max=99999)])
    Tiered_Total = FloatField(label='Tiered Total', validators=[InputRequired(), NumberRange(min=0,max=99999)])
    DeliveryCharges = FloatField(label='Delivery Charges', validators=[InputRequired(), NumberRange(min=0,max=999999)])
    RegulatoryCharges = FloatField(label='Regulatory Charges', validators=[InputRequired(), NumberRange(min=0,max=999999)])
    TotalElectricityCost = FloatField(label='Total Electricity Cost wo h.s.t', validators=[InputRequired(), NumberRange(min=0,max=9999999)])
    submit = SubmitField(label='Next', id="submit_electricity")

class Timeofuse_Form(FlaskForm):

    def validate_Month_Of_bill(self, Month_Of_bill):
        if Month_Of_bill.data < datetime.date(2015,4,1):
            raise ValidationError(
                "Please use a more recent bill!"
            )

    Month_Of_bill = MonthField(u'Month of bill', validators=[InputRequired()])
    TimeofUse_Off_Peak_Value = FloatField(label='Off Peak', validators=[InputRequired(), NumberRange(min=0,max=99999)])
    TimeofUse_Off_Peak_KWH = FloatField(label='KWH', validators=[InputRequired(), NumberRange(min=0,max=99999)])
    TimeofUse_Off_Peak_Total = FloatField(label='Total', validators=[InputRequired(), NumberRange(min=0,max=99999)])
    TimeofUse_Mid_Peak_Value = FloatField(label='Mid Peak', validators=[InputRequired(), NumberRange(min=0,max=99999)])
    TimeofUse_Mid_Peak_KWH = FloatField(label='KWH', validators=[InputRequired(), NumberRange(min=0,max=99999)])
    TimeofUse_Mid_Peak_Total = FloatField(label='Total', validators=[InputRequired(), NumberRange(min=0,max=99999)])
    TimeofUse_On_Peak_Value = FloatField(label='On Peak', validators=[InputRequired(), NumberRange(min=0,max=99999)])
    TimeofUse_On_Peak_KWH = FloatField(label='KWH', validators=[InputRequired(), NumberRange(min=0,max=99999)])
    TimeofUse_On_Peak_Total = FloatField(label='Total', validators=[InputRequired(), NumberRange(min=0,max=99999)])
    DeliveryCharges = FloatField(label='Delivery Charges', validators=[InputRequired(), NumberRange(min=0,max=99999)])
    RegulatoryCharges = FloatField(label='Regulatory Charges', validators=[InputRequired(), NumberRange(min=0,max=99999)])
    TotalElectricityCost = FloatField(label='Total Electricity Cost wo h.s.t', validators=[InputRequired(), NumberRange(min=0,max=9999999)])
    submit = SubmitField(label='Next', id="submit_electricity")