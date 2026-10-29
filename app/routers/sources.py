from fastapi import APIRouter, HTTPException, status, Query, Path
from typing import Annotated

from app.dependencies import source_depends
from app.schemas.sources import SourceRequest, SourceResponse, SourceUpdate



source_router = APIRouter(prefix='/sources', tags=["sources"])



@source_router.post('', status_code=status.HTTP_201_CREATED)
async def add_source(
    source_repo: source_depends,
    source: SourceRequest,
    ) -> None:

    '''
    Take input and validate
    Call repo to add source
    '''
    # TODO : error 
    await source_repo.add_source(source)

"""
@source_router.get('/', status_code=status.HTTP_200_OK)
async def get_active_sources(
    active : Annotated[bool, Query()]
    source_repo: source_depends
    ) -> list[SourceResponse]:
    sources = await source_repo.get_active_sources_from_db()

    if sources is None:
        raise HTTPException(status_code=404, detail='Sources not found')

    return sources
"""
@source_router.get('', status_code=status.HTTP_200_OK)
async def get_sources(
    source_repo: source_depends,
    active : bool | None = Query(default=None)
    ) -> list[SourceResponse]:
    sources = await source_repo.get_sources(active)

    if sources is None:
        raise HTTPException(status_code=404, detail='Sources not found')

    return sources

@source_router.get('/{source_id}', status_code=status.HTTP_200_OK)
async def get_source(
    source_repo: source_depends,
    source_id: Annotated[int, Path(ge=1)]
    ) -> SourceResponse:
    source = await source_repo.get_source(source_id)

    if source is None:
        raise HTTPException(status_code=404, detail='Source not found')

    return source



@source_router.patch('/{source_id}', status_code=status.HTTP_204_NO_CONTENT)
async def update_source(
    source_repo: source_depends,
    source_id: Annotated[int, Path(ge=1)],
    source: SourceUpdate
    ) -> None:

    await source_repo.update_source(source_id, source)


@source_router.delete('/{source_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_source(
    source_repo: source_depends, 
    source_id: Annotated[int, Path(ge=1)]
    ) -> None:

    await source_repo.delete_source(source_id)
