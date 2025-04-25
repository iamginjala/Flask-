from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Float
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.fields.numeric import FloatField
from wtforms.validators import DataRequired
import requests
from flask_migrate import Migrate
from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv("TMDB_API_KEY")

headers = {
    "accept": "application/json",
    "Authorization": api_key
}

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap5(app)

# CREATE DB
class Base(DeclarativeBase):
    pass
db = SQLAlchemy(model_class=Base)

app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///movies-collection.db'

db.init_app(app)
migrate = Migrate(app, db)

MOVIE_DB_IMAGE_URL = "https://image.tmdb.org/t/p/w500"

# CREATE TABLE
class Movie(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True, nullable=False)
    title: Mapped[str] = mapped_column(String,unique=True,nullable=False)
    year: Mapped[int] = mapped_column(Integer,nullable=False)
    description : Mapped[str] = mapped_column(String,nullable=False)
    rating: Mapped[float] = mapped_column(Float,nullable=True)
    ranking : Mapped[int] = mapped_column(Integer,nullable=True)
    review : Mapped[str] = mapped_column(String,nullable=True)
    img_url:Mapped[str] = mapped_column(String,nullable=True)


class EditMovieForm(FlaskForm):
    rating = FloatField("Your Rating Out of 10 e.g. 7.5", validators=[DataRequired()])
    review = StringField("Your Review", validators=[DataRequired()])
    submit = SubmitField("Done")
class AddMovieForm(FlaskForm):
    moviename = StringField("Movie Title",validators=[DataRequired()])
    submit = SubmitField("Add Movie")

@app.route("/")
def home():
    result = db.session.execute(db.select(Movie).order_by(Movie.rating)).scalars().all()
    for i in range(len(result)):
        result[i].ranking = len(result) - i
    db.session.commit()
    return render_template("index.html",movies = result)
@app.route("/add",methods=["GET","POST"])
def add():
    form = AddMovieForm()
    if form.validate_on_submit():
        name = form.moviename.data
        url = f"https://api.themoviedb.org/3/search/movie?query={name}&include_adult=false&language=en-US&page=1"
        response = requests.get(url, headers=headers)
        data = response.json()['results']
        return render_template('select.html',options=data)

    return render_template("add.html",form=form)
@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit(id):
    form = EditMovieForm()
    movie = db.get_or_404(Movie, id)

    if form.validate_on_submit():
        movie.rating = form.rating.data
        movie.review = form.review.data
        db.session.commit()
        return redirect(url_for('home'))

    # Pre-populate form with existing values
    form.rating.data = movie.rating
    form.review.data = movie.review
    return render_template("edit.html", form=form)

@app.route("/<int:id>")
def delete(id):
    movie = db.get_or_404(Movie, id)
    db.session.delete(movie)
    db.session.commit()
    return redirect(url_for('home'))
@app.route('/find')
def find_movie():
    movie_id = request.args.get('id')
    movie_url =f"https://api.themoviedb.org/3/movie/{movie_id}?language=en-US"
    response = requests.get(movie_url,headers=headers)
    data = response.json()
    new_movie = Movie(
        title=data["title"],
        # The data in release_date includes month and day, we will want to get rid of.
        year=data["release_date"].split("-")[0],
        img_url=f"{MOVIE_DB_IMAGE_URL}{data['poster_path']}",
        description=data["overview"]
    )
    db.session.add(new_movie)
    db.session.commit()
    return redirect(url_for("edit",id=new_movie.id))

if __name__ == '__main__':
    app.run(debug=True)
