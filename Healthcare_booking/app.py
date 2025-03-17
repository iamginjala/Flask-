from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from config import Config

# Initialize Flask app
app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

from models import User, Appointment
from routes.auth_routes import auth_bp
from routes.appointment_routes import appointment_bp

# Register Blueprints
app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(appointment_bp, url_prefix='/appointments')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
