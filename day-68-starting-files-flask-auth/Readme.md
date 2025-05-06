# 🔐 Flask Authentication App

A simple web application built with Flask that provides user registration, login, logout, and protected routes using Flask-Login and password hashing via Werkzeug. It also demonstrates role-based navigation visibility and flash messaging.

---

## 🚀 Features

- User Registration with secure password hashing (`pbkdf2:sha256`)
- User Login and Logout using Flask-Login
- Protected Routes (`@login_required`)
- Flash messages for login errors (e.g., incorrect password, email not found)
- Navigation menu changes based on login status
- File download route protected by authentication
- Responsive UI with Bootstrap

---

## 🛠️ Tech Stack

- Python 3
- Flask
- Flask-Login
- Flask SQLAlchemy
- SQLite (local DB)
- Bootstrap 4 (for styling)

---

🔒 Protected Routes
/secrets – Only visible after login

/download – Download file only if authenticated

✨ Flash Message Behavior
Email not found → "The email ID does not exist. Please register."

Wrong password → "Incorrect password. Please try again."

These are shown in a Bootstrap alert in the base layout.

📌 TODOs
Add email validation and confirmation

Add password reset support

Add user profile page

Implement CSRF protection with Flask-WTF (optional)

📃 License
This project is for educational purposes. Modify and reuse as needed.
