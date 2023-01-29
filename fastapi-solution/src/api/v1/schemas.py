"""Схемы представления данных в api"""

from pydantic import BaseModel


class FilmAPI(BaseModel):
    id: str
    title: str
    imdb_rating: str


class FilmData(BaseModel):
    films_actor: list[FilmAPI]
    films_director: list[FilmAPI]
    films_writer: list[FilmAPI]
    