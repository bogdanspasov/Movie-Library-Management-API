from pydantic import BaseModel, constr, StringConstraints
from typing import Annotated
from enum import Enum

class Movie(BaseModel):
    id: int | None = None
    title: str
    director: str
    release_year: int
    rating: float | None = None

    @classmethod
    def from_query_result(cls, id, title, director, release_year, rating):
        return cls(
            id = id,
            title = title,
            director = director,
            release_year = release_year,
            rating = rating
        )



class MovieUpdate(BaseModel):
    title: str
    director: str
    release_year: int
    rating: float | None = None



class MovieResponse(BaseModel):
    id: int
    title: str
    director: str
    release_year: int
    rating: float | None = None



class Role(str, Enum):
    USER = "USER"
    ADMIN = "ADMIN"


TUsername = Annotated[str, StringConstraints(pattern=r'^\w{2,30}$')]


class User(BaseModel):
    id: int | None = None
    username: TUsername
    password: str
    role: Role

    def is_admin(self):
        return self.role == Role.ADMIN

    @classmethod
    def from_query_result(cls, id, username, password, role):
        return cls(
            id = id,
            username = username,
            password = password,
            role = Role(role)
        )



class LoginData(BaseModel):
    username: TUsername
    password: str