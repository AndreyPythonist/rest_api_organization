from uuid import UUID


from pydantic import BaseModel, Field
from pydantic_extra_types.coordinate import Longitude, Latitude


class Activity(BaseModel):
    value: str
    children: list['Activity']


class Coordinates(BaseModel):
    latitude: Latitude
    longitude: Longitude


class PhoneNumbers(BaseModel):
    number: str


class Building(BaseModel):
    address: str
    coordinates: Coordinates


class Organization(BaseModel):
    id: UUID
    name: str
    phone_numbers: list[str]
    building: Building
    activity: list[Activity]
