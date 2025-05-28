from flask import Flask, render_template, request, redirect, session, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from models import db, User, Patient, Doctor, Appointment
from forms import LoginForm, RegisterForm, BookAppointmentForm, VerifyDoctorForm


app = Flask(__name__)
app.secret_key = 'secretkey'  # Replace with environment variable in production
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:password@localhost:5432/healthcare_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db.init_app(app)

with app.app_context():
    db.create_all()

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        existing_user = User.query.filter_by(email=form.email.data).first()
        if existing_user:
            flash("Email already registered.")
            return redirect('/register')

        new_user = User(
            username=form.username.data,
            email=form.email.data,
            password=form.password.data,  # ⚠️ Hash this in real apps!
            role=form.role.data
        )
        db.session.add(new_user)
        db.session.commit()

        flash("Registration successful. Please log in.")
        return redirect('/login')

    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash("Logged in successfully!")  # just a placeholder
        return redirect('/dashboard')
    return render_template('login.html', form=form)


@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    form = VerifyDoctorForm()
    return render_template('dashboard.html', form=form)


@app.route('/verify_doctor', methods=['POST'])
def verify_doctor():
    form = VerifyDoctorForm()
    if form.validate_on_submit():
        # Dummy check or real validation
        return redirect('/doctor_dashboard')
    return redirect('/dashboard')

@app.route('/doctor_dashboard')
def doctor_dashboard():
    # Simulate session-stored doctor_id; replace with real session logic
    doctor_id = session.get('doctor_id', 1)  # fallback to 1 for now
    appointments = Appointment.query.filter_by(doctor_id=doctor_id).order_by(Appointment.appointment_date).all()
    return render_template('doctor.html', appointments=appointments)


@app.route('/patient_dashboard', methods=['GET'])
def patient_dashboard():
    form = BookAppointmentForm()
    return render_template('patient.html', form=form)


@app.route('/book_appointment', methods=['POST'])
def book_appointment():
    form = BookAppointmentForm()
    if form.validate_on_submit():
        # Booking logic can be added here
        flash("Appointment booked!")
    return redirect('/patient_dashboard')


@app.route('/update_appointment/<int:appointment_id>', methods=['POST'])
def update_appointment(appointment_id):
    # approve/cancel logic
    return redirect('/doctor_dashboard')

if __name__ == '__main__':
    app.run(debug=True)
