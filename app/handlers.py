from uuid import UUID
from functools import wraps


from fastapi import APIRouter, Header, Depends
from fastapi.responses import JSONResponse


from app.db.session import async_session
from app.db.dal import OrganizationDAL
from app.schemas import Organization
from app.auth import validate_api_key
from pydantic_extra_types.coordinate import Longitude, Latitude


router = APIRouter(prefix="/v1/organization", tags=['Organization'], dependencies=[Depends(validate_api_key)])

organization = OrganizationDAL(db_session=async_session)


def get_message(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        result = await func(*args, **kwargs)
        if result is None:
            return JSONResponse(content={"message": "Организации не найдены"})
        return result
    return wrapper


@router.get('/list/address/{org_address}', description='Получение организаций находящихся в здании',
            operation_id='GetOrganizationByAddress', response_model=list[Organization])
@get_message
async def get_org_by_building_address(org_address: str):
    return await organization.get_org_by_building_address(building_address=org_address)


@router.get('/list/activity/{activity}', description='Получение организаций по активности',
            operation_id='GetOrganizationByActivity', response_model=list[Organization])
@get_message
async def get_org_by_activity_address(activity: str):
    return await organization.get_org_by_parents_activity(activity=activity)

@router.get('/list/coordinates/{latitude}/{longitude}/{radius}',
            description='Получение организаций находящихся в заданном радиусе относительно переданных координат',
            operation_id='GetOrganizationByCoordinates', response_model=list[Organization])
@get_message
async def get_org_by_coordinates(latitude: Latitude, longitude: Longitude, radius: float):
    return await organization.get_org_by_radius_coordinate(latitude=latitude, longitude=longitude, radius=radius)


@router.get('/id/{id_organization}', description='Получение организации по id',
            operation_id='GetOrganizationById', response_model=Organization)
@get_message
async def get_org_by_id(id_organization: UUID):
    return await organization.get_org_by_id(org_id=id_organization)


@router.get('/list/activity/children/{activity}', description='Получение организаций по вложенным видам активности',
            operation_id='GetOrganizationByChildrenActivity', response_model=list[Organization])
@get_message
async def get_org_by_children_activity(activity: str):
    return await organization.get_org_by_children_activity(activity=activity)


@router.get('/name/{org_name}', description='Получение организации по наименованию',
            operation_id='GetOrganizationByName', response_model=Organization)
@get_message
async def get_org_by_name(org_name: str):
    return await organization.get_org_by_name(name=org_name)
