from uuid import UUID


import asyncio
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from sqlalchemy import select, and_, func
from sqlalchemy.orm import joinedload


from app.db.models import Organization, Building, Activity, ActivityOrganization, Coordinates
from app.db.session import async_session


class OrganizationDAL:
    def __init__(self, db_session: async_sessionmaker[AsyncSession]):
        self.db_session = db_session

    async def get_org_by_name(self, name: str):
        async with self.db_session() as session:
            query = select(Organization).where(Organization.name == name)
            result = await session.execute(query)
            organization = result.scalars().unique().first()
            if organization:
                return await organization.to_dict()

    async def get_org_by_id(self, org_id: UUID):
        async with self.db_session() as session:
            query = select(Organization).where(Organization.id == org_id)
            result = await session.execute(query)
            organization = result.scalars().unique().first()
            if organization:
                return await organization.to_dict()

    async def get_org_by_building_address(self, building_address: str):
        async with self.db_session() as session:
            query = select(Organization).join(Building).where(Building.address == building_address)
            result = await session.execute(query)
            organizations = result.scalars().unique().fetchall()
            if organizations:
                return [await org.to_dict() for org in organizations]

    async def get_org_by_radius_coordinate(self, latitude: float, longitude: float, radius: float):
        async with self.db_session() as session:
            query = select(Organization).join(Building, Organization.building_id == Building.id) \
                    .join(Coordinates, Coordinates.building_id == Building.id) \
                    .where(func.get_distance_from_lat_lon_km(latitude, longitude, Coordinates.latitude,
                                                             Coordinates.longitude) <= radius)
            result = await session.execute(query)
            organizations = result.scalars().unique().fetchall()
            if organizations:
                return [await org.to_dict() for org in organizations]

    async def get_org_by_parents_activity(self, activity: str):
        activity_id = await self._get_activity_id(activity=activity)
        if activity_id is None:
            return
        parents_activity = await self._get_parents_activity(activity_id=activity_id)
        async with self.db_session() as session:
            query = select(Organization) \
                .join(ActivityOrganization, Organization.id == ActivityOrganization.organization_id) \
                .join(Activity, and_(ActivityOrganization.activity_id == Activity.id,
                                     Activity.id.in_(parents_activity)))
            result = await session.execute(query)
            organizations = result.scalars().unique().fetchall()
            if organizations:
                return [await i.to_dict() for i in organizations]

    async def get_org_by_children_activity(self, activity: str):
        activity_id = await self._get_activity_id(activity=activity)
        if activity_id is None:
            return
        children_activity = await self._get_children_activity(activity_id=activity_id)
        async with self.db_session() as session:
            query = select(Organization) \
                .join(ActivityOrganization, Organization.id == ActivityOrganization.organization_id) \
                .join(Activity, and_(ActivityOrganization.activity_id == Activity.id,
                                     Activity.id.in_(children_activity)))
            result = await session.execute(query)
            organizations = result.scalars().unique().fetchall()
            if organizations:
                return [await i.to_dict() for i in organizations]

    async def _get_parents_activity(self, activity_id: str):
        async with self.db_session() as session:
            query = select(Activity).filter(Activity.id == activity_id).cte(name="parents", recursive=True)
            parent_cte = select(Activity).join(query, Activity.id == query.c.parent_id)
            query = query.union_all(parent_cte)
            parent_activities = await session.execute(select(query))
            result = parent_activities.scalars().unique().fetchall()
            if result:
                return result

    async def _get_children_activity(self, activity_id: str):
        async with self.db_session() as session:
            query = select(Activity).filter(Activity.id == activity_id).cte(name="children", recursive=True)
            children_cte = select(Activity).join(query, Activity.parent_id == query.c.id)
            query = query.union_all(children_cte)
            children_activities = await session.execute(select(query))
            result = children_activities.scalars().unique().fetchall()
            if result:
                return result

    async def _get_activity_id(self, activity: str):
        async with self.db_session() as session:
            activity_res = await session.execute(select(Activity).where(Activity.value == activity))
            activity_id = activity_res.scalars().unique().first()
            if activity_id:
                activity_id = activity_id.id
                return activity_id
