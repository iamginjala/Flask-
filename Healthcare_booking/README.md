# Healthcare Booking System

This is a simple healthcare booking system built using Flask and SQLAlchemy. It allows patients to register, log in, and book appointments with doctors.

## Features
- **User Registration and Login**: Users can register as doctors or patients and log in with credentials.
- **Appointment Booking**: Patients can book appointments with doctors.
- **JWT Authentication**: The system uses JSON Web Tokens (JWT) for user authentication.
- **PostgreSQL Database**: The system uses PostgreSQL for database management.

## Project Structure
/healthcare_booking
│── app.py                   # Main Flask application
│── config.py                # Configuration settings (database, secret keys)
│── models.py                # Database models (User, Appointment)
│── routes/
│   ├── auth_routes.py       # Authentication routes (register, login)
│   ├── appointment_routes.py # Appointment booking routes
│── utils.py                 # Helper functions (JWT generation, validation)
│── requirements.txt         # Required dependencies
│── run.py                   # Script to start the Flask app
│── migrations/              # Database migration folder (if using Flask-Migrate)
└── README.md                # Project documentation

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/iamginjala/healthcare_booking.git
   cd healthcare_booking

2. Create a virtual environment:
python3 -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`

3. Install the dependencies:
    pip install -r requirements.txt
4. Set up your PostgreSQL database and configure the DATABASE_URL in the .env file:
    DATABASE_URL=postgresql://user:password@localhost/healthcare_db
    SECRET_KEY=your_secret_key\
5. Run database migrations:
    flask db init
    flask db migrate -m "Initial migration"
    flask db upgrade
6. Start the application:
    python run.py
API Endpoints
Authentication
POST /auth/register: Register a new user (doctor or patient)

Request body: {"username": "user", "password": "password", "role": "doctor"}
POST /auth/login: Login and receive a JWT token

Request body: {"username": "user", "password": "password"}
Response: {"token": "jwt_token"}
Appointments
POST /appointments/: Book an appointment with a doctor
Request headers: Authorization: Bearer <JWT_TOKEN>
Request body: {"doctor_id": 1, "patient_id": 2, "date": "2025-03-17"}
Response: {"message": "Appointment booked successfully"}