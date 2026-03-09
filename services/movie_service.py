from data.database import insert_query, read_query, update_query
from data.models import Movie, MovieResponse, MovieUpdate

def validate_movie(movie):

    if not movie.title or movie.title.strip() == "":
        raise ValueError("Title cannot be empty")

    if movie.release_year < 1888 or movie.release_year > 2115:
        raise ValueError("Invalid release year")

def get_by_id(movie_id: int):
    movie_data = read_query(
        'SELECT id, title, director, release_year, rating FROM movies WHERE id = %s',
        (movie_id,))
    return next((Movie.from_query_result(*row) for row in movie_data), None)


def get_all(title_filter: str | None = None):
    if title_filter:
        data = read_query(
            """SELECT id, title, director, release_year, rating
               FROM movies
               WHERE title LIKE %s""",
            (f"%{title_filter}%",)
        )
    else:
        data = read_query(
            "SELECT id, title, director, release_year, rating FROM movies"
        )
    return [Movie.from_query_result(*row) for row in data]


def sort(lst: list[Movie], reverse=False):
    return sorted(
        lst,
        key=lambda m: m.rating if m.rating is not None else 0,
        reverse=reverse)


def create(movie: Movie):
    validate_movie(movie)
    generated_id = insert_query(
        'INSERT INTO movies(title, director, release_year, rating) VALUES(%s,%s,%s,%s)',
        (movie.title, movie.director, movie.release_year, movie.rating))

    movie.id = generated_id

    return movie


def exists(movie_id: int):
    data = read_query('SELECT 1 from movies where id = %s', (movie_id,))

    return any(data)


def update(movie_update: MovieUpdate, movie: Movie):
    validate_movie(movie_update)
    result = update_query(
        '''UPDATE movies SET
           title = %s, director = %s, release_year = %s, rating = %s
           WHERE id = %s''',
        (movie_update.title, movie_update.director, movie_update.release_year, movie_update.rating, movie.id))

    if result > 0:
        movie.title = movie_update.title
        movie.director = movie_update.director
        movie.release_year = movie_update.release_year
        movie.rating = movie_update.rating
        return movie
    else:
        return None


def delete(movie: Movie):
    update_query('DELETE FROM movies WHERE id = %s', (movie.id,))

