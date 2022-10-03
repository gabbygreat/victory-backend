from sqlmodel import SQLModel, create_engine, Session, select
from models import Expense, ExpenseModel, RoomInfo, Guarantor, Occupant, RoomInfoModel
import os

BASE_DIR = os.path.dirname(os.path.realpath(__file__))
# conn_str = 'sqlite:///'+os.path.join(BASE_DIR, 'hostel.db')
# conn_str = 'postgresql://postgres:gabbygreat1Aheaven4me@localhost/victoryvilla'
conn_str = 'postgres://sbftdttfxzitje:e57a0faaf27fb7e5fb42fcf69be0386dca9f62547e6fea11622b502cb1a8e290@ec2-3-223-242-224.compute-1.amazonaws.com:5432/da8rtdt1sug425'

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
    22: 'A101',
    23: 'A102',
    24: 'A103',
    25: 'A104',
    26: 'A105',
    27: 'A106',
    28: 'A107',
    29: 'A108',
    30: 'B101',
    31: 'B102',
    32: 'B103',
    33: 'B104',
    34: 'B105',
    35: 'B106',
    36: 'B107',
    37: 'B108',
    38: 'B109',
    39: 'C101',
    40: 'C102',
    41: 'C104',
    42: 'C105',
    43: 'A201',
    44: 'A202',
    45: 'A203',
    46: 'A204',
    47: 'A205',
    48: 'A206',
    49: 'A207',
    50: 'A208',
    51: 'B201',
    52: 'B202',
    53: 'B203',
    54: 'B204',
    55: 'B205',
    56: 'B206',
    57: 'B207',
    58: 'B208',
    59: 'B209',
    60: 'C201',
    61: 'C202',
    62: 'C204',
    63: 'C205',
}


class Database:
    def __init__(self) -> None:
        connect_args = {"check_same_thread": False}
        self.engine = create_engine(
            conn_str, echo=True)
        SQLModel.metadata.create_all(self.engine)

    def get_all_rooms(self) -> list[RoomInfoModel]:
        with Session(self.engine) as session:
            rooms = session.exec(select(RoomInfo)).all()
            occupant = session.exec(select(Occupant)).all()
            guarantor = session.exec(select(Guarantor)).all()
            roomInfoModel: list[RoomInfoModel] = []

        for index in range(len(rooms)):
            room_model = RoomInfoModel(
                id=rooms[index].id,
                roomNumber=rooms[index].roomNumber,
                occupied=rooms[index].occupied
            )
            if room_model.occupied:
                room_model.occupant = occupant[index]
                room_model.guarantor = guarantor[index]
            roomInfoModel.append(room_model)

        return {'flag': True, 'data': roomInfoModel}

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
                return {'flag': True, 'data': RoomInfoModel(
                        id=occupant.id,
                        roomNumber=room_number[occupant.id],
                        occupied=False,
                        occupant=None,
                        guarantor=None
                        )}
        return {'flag': False, 'message': 'maximum room length reached !'}

    def update_room_info(self, occupant: Occupant, guarantor: Guarantor, room_id: int):
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

    def get_expenses(self):
        with Session(self.engine) as session:
            expenses = session.exec(select(Expense)).all()
            roomInfoModel: list[ExpenseModel] = []

        return {'flag': True, 'data': expenses}

    def add_expenses(self, expense: ExpenseModel):
        with Session(self.engine) as session:
            expense = Expense(detailOfPayment=expense.detailOfPayment,
                              expenseType=expense.expenseType, date=expense.date, amount=expense.amount)
            session.add(expense)

            session.commit()
            session.refresh(expense)
            return {'flag': True, 'data': ExpenseModel(
                    detailOfPayment=expense.detailOfPayment,
                    expenseType=expense.expenseType,
                    date=expense.date,
                    amount=expense.amount
                    )}
