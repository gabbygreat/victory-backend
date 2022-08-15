from cmath import phase
from sqlmodel import SQLModel, create_engine, Session, select
from models import RoomInfo, Guarantor, Occupant
import os

BASE_DIR = os.path.dirname(os.path.realpath(__file__))
conn_str = 'sqlite:///'+os.path.join(BASE_DIR, 'hostel.db')

room_number: dict = {
    1: 'A001',
    2: 'A002',
    3: 'A003',
    4: 'A004',
    5: 'A005',
    6: 'A006',
    7: 'A007',
    8: 'A008',
    9: 'B001',
    10: 'B002',
    11: 'B003',
    12: 'B004',
    13: 'B005',
    14: 'B006',
    15: 'B007',
    16: 'B008',
    17: 'B009',
    18: 'C001',
    19: 'C002',
    20: 'C004',
    21: 'C005',
}


class Database:
    def __init__(self) -> None:
        connect_args = {"check_same_thread": False}
        self.engine = create_engine(
            conn_str, echo=True, connect_args=connect_args)
        SQLModel.metadata.create_all(self.engine)

    def get_all_rooms(self):
        with Session(self.engine) as session:
            rooms = session.exec(select(RoomInfo)).all()
        return rooms

    def add_room(self):
        if len(self.get_all_rooms()) < 63:
            with Session(self.engine) as session:
                occupant = Occupant()
                session.add(occupant)

                guarantor = Guarantor()
                session.add(guarantor)

                session.commit()

                room = RoomInfo(roomNumber=room_number[occupant.id], occupied=False,
                                occupant_id=occupant.id, guarantor_id=guarantor.id)
                session.add(room)
                session.commit()
                session.refresh(room)
                return room
        return {'flag': False, 'message': 'maximum room length reached !'}

    def update_room_info(self, roomNumber: str, occupied: bool, occupant: Occupant, guarantor: Guarantor, room_id: int):
        with Session(self.engine) as session:
            edit_room = session.get(RoomInfo, room_id)
            edit_occupant = session.get(Occupant, room_id)
            edit_guarantor = session.get(Guarantor, room_id)

            if edit_guarantor and edit_room and edit_occupant:
                edit_room.occupied = True
                session.add(edit_room)

                edit_occupant.name = occupant.name
                edit_occupant.gender = occupant.gender
                edit_occupant.stateOfOrigin = occupant.stateOfOrigin
                edit_occupant.dateOfRentPayment = occupant.dateOfRentPayment
                edit_occupant.phoneNumber = occupant.phoneNumber
                session.add(edit_occupant)

                edit_guarantor.name = guarantor.name
                edit_guarantor.phoneNumber = guarantor.phoneNumber
                session.add(edit_guarantor)

                session.commit()

                return {'flag': True}
            return {"flag": False}

    def clear_room(self, room_id: int):
        with Session(self.engine) as session:
            edit_room = session.get(RoomInfo, room_id)
            edit_occupant = session.get(Occupant, room_id)
            edit_guarantor = session.get(Guarantor, room_id)

            if edit_guarantor and edit_room and edit_occupant:
                edit_room.occupied = False
                session.add(edit_room)

                edit_occupant.name = None
                edit_occupant.gender = None
                edit_occupant.stateOfOrigin = None
                edit_occupant.dateOfRentPayment = None
                edit_occupant.phoneNumber = None
                session.add(edit_occupant)

                edit_guarantor.name = None
                edit_guarantor.phoneNumber = None
                session.add(edit_guarantor)

                session.commit()
                return {'flag': True}
            return {'flag': False}