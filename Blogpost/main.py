import requests

def get_gender_age(name):
    """
    Fetches the predicted gender and age of a person based on their name.

    Parameters:
    name (str): The person's first name.

    Returns:
    tuple: (gender, age) - Predicted gender and age.
    """
    params = {'name': name}

    # Get gender prediction
    res1 = requests.get('https://api.genderize.io/', params=params)
    gender = res1.json().get('gender', 'unknown')  # Default to 'unknown' if not found

    # Get age prediction
    res2 = requests.get('https://api.agify.io/', params=params)
    age = res2.json().get('age', 'unknown')  # Default to 'unknown' if not found

    return gender, age  # Return both values as a tuple
