from typing import Optional
from datetime import datetime
from sqlmodel import SQLModel, Field
from pydantic import BaseModel


class Occupant(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: Optional[str] = Field(default=None)
    gender: Optional[str] = Field(default=None)
    phoneNumber: Optional[str] = Field(default=None)
    stateOfOrigin: Optional[str] = Field(default=None)
    dateOfRentPayment: Optional[datetime] = Field(default=None)


class Guarantor(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: Optional[str] = Field(default=None)
    phoneNumber: Optional[str] = Field(default=None)


class RoomInfo(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    roomNumber: str
    occupied: bool
    price: int
    occupant_id: Optional[int] = Field(
        default=None, foreign_key='occupant.id',)
    guarantor_id: Optional[int] = Field(
        default=None, foreign_key='guarantor.id')


class Expense(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    detailOfPayment: str
    expenseType: str
    amount: int
    date: datetime


class OccupantModel(BaseModel):
    name: str
    gender: str
    phoneNumber: str
    stateOfOrigin: str
    dateOfRentPayment: datetime


class GuarantorModel(BaseModel):
    name: str
    phoneNumber: str


class RoomInfoModel(BaseModel):
    id: int
    roomNumber: str
    occupied: bool
    price: int
    occupant: OccupantModel | None = None
    guarantor: GuarantorModel | None = None


class ExpenseModel(BaseModel):
    detailOfPayment: str
    expenseType: str
    amount: int
    date: datetime
