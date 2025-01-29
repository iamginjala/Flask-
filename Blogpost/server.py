from flask import Flask, render_template
from main import get_gender_age  # Import function from main.py

# Initialize Flask app
app = Flask(__name__)

@app.route('/guess/<name>')  # Route to handle name-based predictions
def guess(name):
    """
    Flask route to predict a user's gender and age based on their name.

    Parameters:
    name (str): The name input from the user.

    Returns:
    HTML page with the predicted gender and age.
    """
    gender, age = get_gender_age(name)  # Call function from main.py
    return render_template('index.html', name=name, gender=gender, age=age)

if __name__ == "__main__":
    app.run(debug=True)  # Run Flask app in debug mode
