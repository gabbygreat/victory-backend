from datetime import datetime
from fastapi import FastAPI, Body

from database import Database
from models import Guarantor, Occupant, RoomInfo, RoomInfoModel

app = FastAPI()
database = Database()


@app.get('/')
async def home():
    return datetime.now()


@app.get('/api/rooms')
async def get_all_rooms() -> list[RoomInfoModel]:
    return database.get_all_rooms()


@app.post('/api/rooms')
async def add_room():
    return database.add_room()


@app.post('/api/rooms/{room_id}')
async def update_room_info(room_id: int, occupant: Occupant, guarantor: Guarantor):
    return database.update_room_info(room_id=room_id, occupant=occupant, guarantor=guarantor)


@app.post('/api/clear/{room_id}')
async def clear_room(room_id: int):
    return database.clear_room(room_id=room_id)


@app.get('/api/expense')
async def get_expenses():
    return database.get_expenses()


@app.post('/api/expense')
async def add_expenses(detailOfPayment: str, expenseType: str, amount: int, date: datetime):
    return database.add_expenses(detailOfPayment=detailOfPayment, expenseType=expenseType, date=date, amount=amount)
