from datetime import datetime
from fastapi import FastAPI, Body

from database import Database
from models import Guarantor, Occupant, RoomInfo, RoomInfoModel

app = FastAPI()
database = Database()


@app.get('/')
async def home():
    return datetime.now()


@app.get('/rooms')
async def get_all_rooms() -> list[RoomInfoModel]:
    return database.get_all_rooms()


@app.post('/rooms')
async def add_room():
    return database.add_room()


@app.post('/rooms/{room_id}')
async def update_room_info(room_id: int, occupant: Occupant, guarantor: Guarantor):
    return database.update_room_info(room_id=room_id, occupant=occupant, guarantor=guarantor)


@app.post('/clear/{room_id}')
async def clear_room(room_id: int):
    return database.clear_room(room_id=room_id)
