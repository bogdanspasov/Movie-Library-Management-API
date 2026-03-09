import unittest
from unittest.mock import patch
from services import movie_service
from data.models import Movie, MovieUpdate


class TestMovieService(unittest.TestCase):

    @patch("services.movie_service.insert_query")
    def test_create_movie(self, mock_insert):
        mock_insert.return_value = 10

        movie = Movie(
            title="Inception",
            director="Nolan",
            release_year=2010,
            rating=None
        )

        created = movie_service.create(movie)

        self.assertEqual(created.id, 10)
        self.assertEqual(created.title, "Inception")

    @patch("services.movie_service.read_query")
    def test_get_by_id_found(self, mock_read):
        mock_read.return_value = [
            (1, "Matrix", "Wachowski", 1999, 8.7)
        ]

        movie = movie_service.get_by_id(1)

        self.assertIsNotNone(movie)
        self.assertEqual(movie.title, "Matrix")

    @patch("services.movie_service.read_query")
    def test_get_by_id_not_found(self, mock_read):
        mock_read.return_value = []

        movie = movie_service.get_by_id(1)

        self.assertIsNone(movie)

    @patch("services.movie_service.read_query")
    def test_get_all_movies(self, mock_read):
        mock_read.return_value = [
            (1, "Matrix", "Wachowski", 1999, 8.7),
            (2, "Inception", "Nolan", 2010, 8.8),
        ]

        movies = movie_service.get_all()

        self.assertEqual(len(movies), 2)

    @patch("services.movie_service.update_query")
    def test_update_movie(self, mock_update):
        mock_update.return_value = 1

        movie = Movie(
            id=1,
            title="Old",
            director="Dir",
            release_year=2000,
            rating=None
        )

        update = MovieUpdate(
            title="New",
            director="Dir",
            release_year=2001,
            rating=7.5
        )

        result = movie_service.update(update, movie)

        self.assertEqual(result.title, "New")
        self.assertEqual(result.release_year, 2001)

    @patch("services.movie_service.update_query")
    def test_delete_movie(self, mock_delete):
        movie = Movie(
            id=1,
            title="Test",
            director="Dir",
            release_year=2000,
            rating=None
        )

        movie_service.delete(movie)

        mock_delete.assert_called_once()