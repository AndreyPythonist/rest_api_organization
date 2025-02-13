import uuid

from sqlalchemy import Column, ForeignKey, VARCHAR, DECIMAL
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, DeclarativeBase
from sqlalchemy.ext.asyncio import AsyncAttrs


class Base(AsyncAttrs, DeclarativeBase):
    pass


class Organization(Base):
    __tablename__ = "organization"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    building_id = Column(UUID(as_uuid=True), ForeignKey("building.id"), nullable=False)
    name = Column(VARCHAR(255), nullable=False, unique=True)
    phone_numbers = relationship("PhoneNumber", back_populates="organization", lazy="joined")
    building = relationship("Building", back_populates="organization", lazy="joined")
    activity = relationship("Activity", "activity_organization", back_populates="organization",
                            lazy="joined")

    async def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "phone_numbers": [i.number for i in self.phone_numbers],
            "building": self.building.to_dict(),
            "activity": [await i.to_dict() for i in self.activity]
        }


class PhoneNumber(Base):
    __tablename__ = "phone_number"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    organization_id = Column(UUID(as_uuid=True), ForeignKey("organization.id"), nullable=False)
    organization = relationship("Organization", back_populates="phone_numbers")
    number = Column(VARCHAR(30), nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "number": self.number
        }


class Building(Base):
    __tablename__ = "building"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    organization = relationship("Organization", back_populates="building")
    address = Column(VARCHAR(255), nullable=False)
    coordinates = relationship("Coordinates", back_populates="building", lazy="joined")

    def to_dict(self):
        return {
            "id": self.id,
            "address": self.address,
            "coordinates": self.coordinates[0].to_dict()
        }


class Coordinates(Base):
    __tablename__ = "coordinates"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    building_id = Column(UUID(as_uuid=True), ForeignKey("building.id"), unique=True, nullable=False)
    building = relationship("Building", back_populates="coordinates")
    latitude = Column(DECIMAL(8,6), nullable=False)
    longitude = Column(DECIMAL(9,6), nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "latitude": self.latitude,
            "longitude": self.longitude
        }


class Activity(Base):
    __tablename__ = "activity"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    parent_id = Column(UUID(as_uuid=True), ForeignKey("activity.id"), nullable=True)
    organization = relationship("Organization", "activity_organization", back_populates="activity",
                                lazy="joined")
    children = relationship("Activity", back_populates="parent", lazy="joined")
    parent = relationship("Activity", back_populates="children", remote_side=[id], lazy="joined")
    value = Column(VARCHAR(255), nullable=False)

    async def to_dict(self):
        return {
            "id": self.id,
            "value": self.value,
            "children": [await self.get_children_activity(child) for child in await self.awaitable_attrs.children]
        }

    @staticmethod
    async def get_children_activity(child):
        if not child:
            return []

        return await child.to_dict()


class ActivityOrganization(Base):
    __tablename__ = "activity_organization"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    organization_id = Column(UUID(as_uuid=True), ForeignKey("organization.id"))
    activity_id = Column(UUID(as_uuid=True), ForeignKey("activity.id"))
