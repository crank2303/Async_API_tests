from http import HTTPStatus
from typing import Optional,Union
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Response

from api.v1.utils import PersonParams, PersonSearchParams
from api.v1.schemas import FilmAPI, FilmData
from api.v1.contstants import NO_PERSON, PERSON_NOT_FOUND
from models.person import Person
from services.persons import PersonService, get_person_service
from services.film import FilmService, get_film_service


router = APIRouter()


@router.get(
    path='/',
    response_model=list[Person],
    summary='Полный перечень людей',
    description='Полный перечень людей',
    response_description='Список с полной информацией фильмов в которых принимали участие',
)
async def get_persons(
    params: PersonParams = Depends(),
    person_service: PersonService = Depends(get_person_service),
) -> list[Person]:

    es_persons = await person_service.get_list(params)
    if not es_persons:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=NO_PERSON)
    
    #persons = await prepare_person(es_persons)
    persons = es_persons
    
    if params.sort:
        rev = False if '-' in params.sort else True
        params.sort = params.sort.replace('-', '')
        persons = sorted(persons, key=lambda x: x.dict()[params.sort], reverse=rev)
    return persons


@router.get(
    path='/search',
    response_model=list[Person],
    summary='Поиск по имени',
    description='Поиск по имени',
    response_description='Список ревелантных результатов',
)
async def get_search_persons(
    params: PersonSearchParams = Depends(),
    person_service: PersonService = Depends(get_person_service),
) -> list[Person]:

    es_persons = await person_service.get_search_list(params)
    if not es_persons:
        return Response(content='[]', media_type="application/json")
    
    # persons = await prepare_person(es_persons)
    persons = es_persons
    return persons


@router.get(
    '/{uuid}',
    response_model=Optional[Person],
    summary='Поиск актера по UUID',
    description='Поиск актера по UUID',
    response_description='Полная информация о человеке',
)
async def person_details(
    uuid: str, 
    person_service: PersonService=Depends(get_person_service)
) -> Optional[Person]:
    es_person = await person_service.get_by_id(uuid)
    if not es_person:
        return Response(content='[]', media_type="application/json")

    # person = await prepare_person([es_person])
    person = es_person
    return person


@router.get(
    '/{uuid}/film',
    response_model=list[FilmData],
    summary='Информация о фильмах',
    description='Информация о всех фильмах в которых человек принимал участие',
    response_description='Полная информация о фильмах',
)
async def person_films(
    uuid: str, 
    person_service: PersonService=Depends(get_person_service),
    film_service: FilmService=Depends(get_film_service),
    ) -> list[FilmData]:
    '''Формирует подробную информаю о фильмах которые/которых снимался человек
    
    Args:
        uuid: id человека
        person_service: экземляр класса PersonService
        film_service: экземляр класса FilmService

    Return:
        list[FilmData]: список информации о фильмах по опрделенной роли
    '''

    person_roles: Person = await person_details(uuid, person_service) 
    role_films = {}
    if isinstance(person_roles, Response):
        return Response(content='[]', media_type="application/json")

    films = {
        'actor': person_roles.film_ids_actor,
        'director': person_roles.film_ids_director,
        'writer': person_roles.film_ids_writer,
    }
    

    for role, film_list in films.items() :
        films_info = await get_film_info(film_list, film_service)
        role_films['films_'+role] = films_info
    rez = [FilmData(**role_films)]
    return rez


async def get_film_info(
    films_ids: list[str],
    film_service: FilmService=Depends(get_film_service),
    )->list[FilmAPI]:
    '''Получает данные по одной роли о фильмах из es
    
    Args:
        films_ids: id фильмов
        film_service: экземпляр класса FilmService

    Return:
        list[FilmAPI]: список информации о фильмах
    '''

    films_data = []
    for film_id in films_ids:
        es_film = await film_service.get_by_id(film_id)
        films_data.append(FilmAPI(id=es_film.id,
                                title=es_film.title,
                                imdb_rating=es_film.imdb_rating
                                ))
    return films_data
