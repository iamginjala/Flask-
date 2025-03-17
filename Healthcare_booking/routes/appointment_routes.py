from flask import Blueprint, request, jsonify
from models import db, Appointment
import jwt
from config import Config


def verify_token(token):
    try:
        payload = jwt.decode(token, Config.SECRET_KEY, algorithms=['HS256'])
        return payload
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None
    except Exception:
        return None


appointment_bp = Blueprint('appointments', __name__)


@appointment_bp.route('/', methods=['POST'])
def book_appointment():
    token = request.headers.get('Authorization')
    if not token:
        return jsonify({'message': 'Token is missing'}), 401

    payload = verify_token(token)
    if not payload:
        return jsonify({'message': 'Invalid or expired token'}), 401

    data = request.get_json()
    if not data or 'doctor_id' not in data or 'patient_id' not in data or 'date' not in data:
        return jsonify({'message': 'Missing required fields'}), 400

    new_appointment = Appointment(doctor_id=data['doctor_id'], patient_id=data['patient_id'], date=data['date'])
    db.session.add(new_appointment)
    db.session.commit()
    return jsonify({'message': 'Appointment booked successfully'}), 201
