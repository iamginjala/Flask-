# Flask Name Guessing App

This is a simple Flask web application that predicts a person's **gender** and **age** based on their name. It uses two external APIs:  
- [Genderize API](https://genderize.io/) (for predicting gender)  
- [Agify API](https://agify.io/) (for predicting age)  


## **Installation & Usage**
### **1. Clone the Repository**

1.git clone https://github.com/iamginjala/flask-name-guessing.git
cd flask-name-guessing

2.Install Dependencies

Make sure you have Python installed, then install Flask:
pip install flask requests

3.Run the Flask App

python server.py

4. Test the App
Open your browser and go to: http://127.0.0.1:5000/guess/John
Replace "John" with any name to see predictions.

How It Works
server.py handles the Flask routes and renders HTML pages.
main.py fetches data from the APIs.
The data is passed to index.html, which displays the results.

API References

Genderize.io
Agify.io
