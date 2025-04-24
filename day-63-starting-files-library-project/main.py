
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Float

'''
Red underlines? Install the required packages first: 
Open the Terminal in PyCharm (bottom left). 

On Windows type:
python -m pip install -r requirements.txt

On MacOS type:
pip3 install -r requirements.txt

This will install the packages from requirements.txt for this project.
'''
class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///library-books.db"

db.init_app(app)

class Book(db.Model):
    id : Mapped[int] = mapped_column(Integer,primary_key=True,nullable=False)
    title : Mapped[str] = mapped_column(String(250),nullable=False,unique=True)
    author : Mapped[str] = mapped_column(String(250),nullable=False)
    rating : Mapped[float] = mapped_column(Float,nullable=False)

all_books = []

with app.app_context():
    db.create_all()
# with app.app_context():
#   result = db.session.execute(db.select(Books).order_by(Books.title))
#   all_books = result.scalars().all()
@app.route('/')
def home():
    with app.app_context():
        result = db.session.execute(db.select(Book).order_by(Book.id))
        all_books = result.scalars().all()
    return render_template('index.html',books=all_books)


@app.route("/add",methods=['GET','POST'])
def add():
    if request.method == 'POST':
        with app.app_context():
            new_book = Book(title=request.form.get('book_name'),author=request.form.get('author_name'),rating=request.form.get('rating'))
            db.session.add(new_book)
            db.session.commit()
        return redirect(url_for('home'))
    return render_template('add.html')
@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit_rating(id):
    book = db.get_or_404(Book, id)  # fetches the book or 404

    if request.method == "POST":
        new_rating = request.form.get("rating")
        if new_rating:
            book.rating = float(new_rating)
            db.session.commit()
        return redirect(url_for("home"))

    return render_template("edit.html", book=book)
@app.route("/<int:id>")
def delete_book(id):
    book = db.get_or_404(Book,id)
    db.session.delete(book)
    db.session.commit()

    return redirect(url_for('home'))

if __name__ == "__main__":
    app.run(debug=True)

