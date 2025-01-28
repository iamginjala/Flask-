from flask import Flask
import random
app = Flask(__name__)
def make_bold(func):
    def wrapper():
        return "<b>" + func() + "</b>"
    return wrapper
def make_h1(func):
    def wrapper():
        return "<h1>" + func() + "</h1>"
    return wrapper
@make_bold
@make_h1
@app.route('/')
def home_page():
    return ("<h1>Guess a number between 0 and 9</h1>"
            "<img src=https://media.giphy.com/media/3o7aCSPqXE5C6T8tBC/giphy.gif>")
answer =  random.randint(0,9)
@app.route('/<int:number>')
def guess_number(number):
    if number < answer:
        return ("<h1 style= 'color:red'>" + f"{number} is too low" + "</h1>"
                "<img src= https://media.giphy.com/media/jD4DwBtqPXRXa/giphy.gif>")

    elif number > answer:
        return ("<h1 style= 'color:purple'>" + f"{number} is too high" +"</h1>"
                "<img src=https://media.giphy.com/media/3o6ZtaO9BZHcOjmErm/giphy.gif>")
    else:
        return ("<h1 style= 'color:green'>""you found me"+"</h1>"
                "<img src=https://media.giphy.com/media/4T7e4DmcrP9du/giphy.gif>")

if __name__ == '__main__':
    app.run(debug=True)