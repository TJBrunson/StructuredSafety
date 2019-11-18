from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SelectField, SubmitField, FormField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from app.models import User, Company, Address

class UserLoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    passwordCheck = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Username taken, please try another!')
    
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('An account with this email already exists. Please use another email.')

class CompanyRegistrationForm(FlaskForm):
    company_name = StringField('Company Name', validators=[DataRequired()])

class AddressForm(FlaskForm):
    address_1 = StringField('Address 1', validators=[DataRequired()])
    address_2 = StringField('Address 2')
    city = StringField('City/Provence', validators=[DataRequired()])
    state = StringField('State', validators=[DataRequired()])
    postal_code = StringField('Postal Code', validators=[DataRequired()])

class NewCompanyRegistrationForm(FlaskForm):
    company_info = FormField(CompanyRegistrationForm)
    company_address = FormField(AddressForm)