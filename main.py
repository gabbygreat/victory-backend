from datetime import datetime
from fastapi import FastAPI, Body

from database import Database
from models import Guarantor, Occupant, RoomInfo

app = FastAPI()
database = Database()


@app.get('/')
async def home():
    return datetime.now()


@app.get('/rooms')
async def get_all_rooms():
    return database.get_all_rooms()


@app.post('/rooms')
async def add_room():
    return database.add_room()


@app.post('/rooms/{room_id}')
async def update_room_info(room_id: int, occupant: Occupant, guarantor: Guarantor, occupied: bool = Body(embed=True), roomNumber: str = Body(embed=True),):
    return database.update_room_info(room_id=room_id, roomNumber=roomNumber, occupant=occupant, guarantor=guarantor, occupied=occupied)


@app.post('/clear/{room_id}')
async def clear_room(room_id: int):
    return database.clear_room(room_id=room_id)
