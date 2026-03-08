from fastapi import APIRouter, Header, BackgroundTasks
from common.responses import BadRequest, InternalServerError, NoContent, NotFound, Unauthorized, Forbidden
from common.auth import get_user_or_raise_401
from data.models import Movie, MovieResponse, MovieUpdate
from services import movie_service
from services import OMDb_service

movies_router = APIRouter(prefix='/movies')

@movies_router.post('/')
def create_movie(
        movie: Movie,
        background_tasks: BackgroundTasks,
        x_token=Header()
):

    user = get_user_or_raise_401(x_token)
    if not user.is_admin():
        return Forbidden('Only Admins can add movies')

    created_movie = movie_service.create(movie)

    background_tasks.add_task(
        OMDb_service.enrich_movie_rating,
        created_movie.id,
        created_movie.title
    )

    return created_movie



@movies_router.get('/')
def get_all_movies(
        title: str | None = None,
        sort: str | None = None,
        x_token=Header()
):
    user = get_user_or_raise_401(x_token)

    movies = movie_service.get_all(title_filter=title)

    if sort in ("asc", "desc"):
        movies = movie_service.sort(movies, reverse=(sort == "desc"))

    return movies



@movies_router.get('/{id}')
def get_movie_by_id(id: int, x_token=Header()):
    user = get_user_or_raise_401(x_token)

    movie = movie_service.get_by_id(id)

    if movie is None:
        return Forbidden(f"Movie with id {id} not found")
    else:
        return movie



@movies_router.delete('/{id}')
def delete_movie(id: int, x_token=Header()):
    user = get_user_or_raise_401(x_token)
    if not user.is_admin():
        return Forbidden('Only Admins can delete movies')

    movie = movie_service.get_by_id(id)
    # if not movie:
    #     return NotFound(f"Movie with id {id} not found")

    movie_service.delete(movie)
    return NoContent()



@movies_router.put('/{id}')
def update_movie(id: int, update_data: MovieUpdate, x_token=Header()):
    user = get_user_or_raise_401(x_token)

    if not user.is_admin():
        return Unauthorized('Only Admins can edit movies')

    movie = movie_service.get_by_id(id)
    if not movie:
        return NotFound(f"Movie with id {id} not found")

    updated_movie = movie_service.update(update_data, movie)

    if not updated_movie:
        return InternalServerError()

    return updated_movie
