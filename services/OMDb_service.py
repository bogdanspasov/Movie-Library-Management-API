import requests
from data.database import update_query

OMDB_API_KEY = "ce9fc853"


def enrich_movie_rating(movie_id: int, title: str):

    url = f"http://www.omdbapi.com/?t={title}&apikey={OMDB_API_KEY}"

    try:
        response = requests.get(url)
        data = response.json()

        rating = None

        if data.get("imdbRating") and data["imdbRating"] != "N/A":
            rating = float(data["imdbRating"])

        update_query(
            "UPDATE movies SET rating = %s WHERE id = %s",
            (rating, movie_id)
        )

    except Exception:
        # fail gracefully if API fails
        pass