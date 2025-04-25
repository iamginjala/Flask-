## 🎬 Movie Collection App

This is a Flask web application that lets users search, add, edit, review, rank, and delete movies from their personal movie collection using data pulled from The Movie Database (TMDB) API.
The project uses Flask, Flask-WTF for forms, Flask-Bootstrap for styling, SQLAlchemy for database management, and Flask-Migrate for migrations.

## 🚀 Features
Home Page: Displays your favorite movies with rankings, posters, ratings, reviews, and descriptions.

Add Movie: Search for a movie using TMDB API and add it to your database.

Edit Movie: Update the movie’s rating and review.

Delete Movie: Remove a movie from your collection.

Responsive UI: Built with custom CSS and Bootstrap for a clean and modern look.

## 🛠️ Tech Stack
Backend: Python, Flask

Frontend: HTML, CSS, Bootstrap 5

Database: SQLite (with SQLAlchemy ORM)

API Integration: TMDB API (https://api.themoviedb.org/3)

Forms: Flask-WTF

Database Migrations: Flask-Migrate

## 📂 Project Structure

├── static/
│   └── css/
│       └── styles.css   # Custom styles
├── templates/
│   ├── base.html        # Base template with Bootstrap and common layout
│   ├── index.html       # Home page displaying all movies
│   ├── add.html         # Form to search and add a movie
│   ├── select.html      # List of movies to select after search
│   ├── edit.html        # Form to edit rating and review
├── movies-collection.db # SQLite database (auto-created)
├── main.py              # Main Flask application
├── README.md            # This file

## 🔑 Setup Instructions

### 1. Clone the repository


git clone https://www.github.com/iamginjala/Flask-



### 2. Install dependencies
pip install -r requirements.txt

### 3. Required packages:

Flask

Flask-SQLAlchemy

Flask-WTF

Flask-Bootstrap

Flask-Migrate

Requests