import os

import requests
from data_manager import DataManager
from dotenv import load_dotenv
from flask import Flask, render_template, request, redirect, url_for
from models import Movie, db, User


load_dotenv()
OMDB_KEY = os.getenv("OMDB_KEY")
OMDB_URL = "http://www.omdbapi.com/"

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config["SQLALCHEMY_DATABASE_URI"] = (
    f"sqlite:///{os.path.join(basedir, 'data/movies.db')}"
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(
    app
)  # Link the database and the app. This is the reason you need to import db from models

data_manager = DataManager()  # Create an object of your DataManager class


@app.route("/", methods=["GET"])
def index():
    """Show a list of all registered users and a form for adding new users."""
    users = data_manager.get_users()
    return render_template("index.html", users=users)


@app.route("/users", methods=["POST"])
def create_user():
    """When the user submits the “add user” form, a POST request is made.
    The server receives the new user info, adds it to the database, then redirects back to /.
    """
    name = request.form.get("name")
    data_manager.create_user(name)
    return redirect(url_for("index")), 200


@app.route("/users/<int:user_id>/movies", methods=["GET"])
def get_movies(user_id):
    """When you click on a user name, the app retrieves that user’s list of favorite movies and displays it."""
    movies = data_manager.get_movies(user_id)
    user = User.query.get(user_id)
    return render_template("movies.html", movies=movies, user=user)


@app.route("/users/<int:user_id>/movies", methods=["POST"])
def add_movie(user_id):
    """Add a new movie to a user’s list of favorite movies."""
    title = request.form.get("title")

    params = {"apikey": OMDB_KEY, "t": title}
    response = requests.get(OMDB_URL, params=params)
    movie_info = response.json()

    new_movie = Movie(
        name=movie_info["Title"],
        director=movie_info["Director"],
        year=movie_info["Year"],
        poster_url=movie_info["Poster"],
        user_id=user_id,
    )
    data_manager.add_movie(new_movie)
    return redirect(url_for("get_movies", user_id=user_id)), 303


@app.route("/users/<int:user_id>/movies/<int:movie_id>/update", methods=["POST"])
def update_movie(user_id, movie_id):
    """Modify the title of a specific movie in a user’s list, without depending on OMDb for corrections."""
    new_title = request.form.get("title")
    data_manager.update_movie(movie_id=movie_id, new_title=new_title)
    return redirect(url_for("get_movies", user_id=user_id)), 303


@app.route("/users/<int:user_id>/movies/<int:movie_id>/delete", methods=["POST"])
def delete_movie(user_id, movie_id):
    """Remove a specific movie from a user’s favorite movie list."""
    data_manager.delete_movie(movie_id)
    return redirect(url_for("get_movies", user_id=user_id)), 303


if __name__ == "__main__":
    with app.app_context():
        db.create_all()

    app.run()
