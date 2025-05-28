# healthcare_booking/forms.py
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField, IntegerField, DateField, TimeField
from wtforms.validators import DataRequired, Email, EqualTo

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    role = SelectField('Role', choices=[('doctor', 'Doctor'), ('patient', 'Patient')], validators=[DataRequired()])
    submit = SubmitField('Register')

class BookAppointmentForm(FlaskForm):
    doctor_id = IntegerField('Doctor ID', validators=[DataRequired()])
    appointment_date = DateField('Date', validators=[DataRequired()])
    appointment_time = TimeField('Time', validators=[DataRequired()])
    submit = SubmitField('Book Appointment')

class VerifyDoctorForm(FlaskForm):
    doctor_id = IntegerField('Enter Doctor ID', validators=[DataRequired()])
    submit = SubmitField('Continue as Doctor')
