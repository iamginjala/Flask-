from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import os

# Ensure the 'database/' directory exists
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DB_FOLDER = os.path.join(BASE_DIR, "database")
DB_PATH = os.path.join(DB_FOLDER, "expenses.db")

if not os.path.exists(DB_FOLDER):
    os.makedirs(DB_FOLDER)  # ✅ Ensure database folder exists

app = Flask(__name__)

# ✅ Set SQLAlchemy configuration BEFORE initializing db
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{DB_PATH}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# ✅ Import models AFTER defining 'app'
from models import db, Expense

# ✅ Initialize SQLAlchemy with the Flask app
db.init_app(app)  # ✅ Register the app with db

@app.route('/')
def index():
    expenses = Expense.query.all()
    return render_template('index.html', expenses=expenses)

@app.route('/add', methods=['POST'])
def add_expense():
    title = request.form['title']
    amount = float(request.form['amount'])
    category = request.form['category']
    new_expense = Expense(title=title, amount=amount, category=category)
    db.session.add(new_expense)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/delete/<int:id>')
def delete_expense(id):
    expense = Expense.query.get(id)
    if expense:
        db.session.delete(expense)
        db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # ✅ Ensure database tables are created
    app.run(debug=True)

