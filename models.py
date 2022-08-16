from typing import Optional
from datetime import datetime
from sqlmodel import SQLModel, Field
from pydantic import BaseModel

class Occupant(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: Optional[str] = Field(default=None)
    gender: Optional[str]= Field(default=None)
    phoneNumber: Optional[int]= Field(default=None)
    stateOfOrigin: Optional[str]= Field(default=None)
    dateOfRentPayment: Optional[datetime]= Field(default=None)

class Guarantor(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: Optional[str] = Field(default=None)
    phoneNumber: Optional[int] = Field(default=None)

class RoomInfo(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    roomNumber: str
    occupied: bool
    occupant_id: Optional[int] = Field(default=None, foreign_key='occupant.id')
    guarantor_id: Optional[int] = Field(default=None, foreign_key='guarantor.id')


class OccupantModel(BaseModel):
    name: str
    gender: str
    phoneNumber: int
    stateOfOrigin: str
    dateOfRentPayment: datetime

class GuarantorModel(BaseModel):
    name: str
    phoneNumber: int

class RoomInfoModel(BaseModel):
    id: int
    roomNumber: str
    occupied: bool
    occupant: OccupantModel | None = None
    guarantor: GuarantorModel | None = None
