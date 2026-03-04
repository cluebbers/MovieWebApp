from models import Movie, User, db


class DataManager:
    # Define Crud operations as methods
    def create_user(self, name):
        """Add a new user to your database."""
        new_user = User(name=name)
        db.session.add(new_user)
        db.session.commit()

    def get_users(self):
        """Return a list of all users in your database."""
        return User.query.all()

    def get_movies(self, user_id):
        """Return a list of all movies of a specific user."""
        return Movie.query.filter_by(user_id=user_id).all()

    def add_movie(self, movie):
        """Add a new movie to a user’s favorites."""
        db.session.add(movie)
        db.session.commit()

    def update_movie(self, movie_id, new_title):
        """Update the details of a specific movie in the database."""
        movie = Movie.query.get(movie_id)
        movie.name = new_title
        db.session.commit()
        

    def delete_movie(self, movie_id):
        """Delete the movie from the user’s list of favorites."""
        movie = Movie.query.get(movie_id)
        db.session.delete(movie)
        db.session.commit()
