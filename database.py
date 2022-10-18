from sqlmodel import SQLModel, create_engine, Session, select
from models import Expense, ExpenseModel, RoomInfo, Guarantor, Occupant, RoomInfoModel
import os

BASE_DIR = os.path.dirname(os.path.realpath(__file__))
# conn_str = 'sqlite:///'+os.path.join(BASE_DIR, 'hostel.db')
conn_str = 'postgresql://postgres:gabbygreat1Aheaven4me@localhost/victory'
# conn_str = 'postgresql://sbftdttfxzitje:e57a0faaf27fb7e5fb42fcf69be0386dca9f62547e6fea11622b502cb1a8e290@ec2-3-223-242-224.compute-1.amazonaws.com:5432/da8rtdt1sug425'

room_number: dict[int, list[str]] = {
    1: ['A001', 230000],
    2: ['A002', 230000],
    3: ['A003', 230000],
    4: ['A004', 230000],
    5: ['A005', 230000],
    6: ['A006', 230000],
    7: ['A007', 230000],
    8: ['A008', 230000],
    9: ['B001', 230000],
    10: ['B002', 230000],
    11: ['B003', 230000],
    12: ['B004', 230000],
    13: ['B005', 230000],
    14: ['B006', 210000],
    15: ['B007', 230000],
    16: ['B008', 230000],
    17: ['B009', 230000],
    18: ['C001', 250000],
    19: ['C002', 230000],
    20: ['C004', 230000],
    21: ['C005', 230000],
    22: ['A101', 230000],
    23: ['A102', 230000],
    24: ['A103', 230000],
    25: ['A104', 230000],
    26: ['A105', 230000],
    27: ['A106', 230000],
    28: ['A107', 230000],
    29: ['A108', 230000],
    30: ['B101', 230000],
    31: ['B102', 230000],
    32: ['B103', 230000],
    33: ['B104', 230000],
    34: ['B105', 230000],
    35: ['B106', 210000],
    36: ['B107', 230000],
    37: ['B108', 230000],
    38: ['B109', 230000],
    39: ['C101', 250000],
    40: ['C102', 230000],
    41: ['C104', 230000],
    42: ['C105', 230000],
    43: ['A201', 230000],
    44: ['A202', 230000],
    45: ['A203', 230000],
    46: ['A204', 230000],
    47: ['A205', 230000],
    48: ['A206', 230000],
    49: ['A207', 230000],
    50: ['A208', 230000],
    51: ['B201', 230000],
    52: ['B202', 230000],
    53: ['B203', 230000],
    54: ['B204', 230000],
    55: ['B205', 230000],
    56: ['B206', 210000],
    57: ['B207', 230000],
    58: ['B208', 230000],
    59: ['B209', 230000],
    60: ['C201', 250000],
    61: ['C202', 230000],
    62: ['C204', 230000],
    63: ['C205', 230000],
}


class Database:
    def __init__(self) -> None:
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
                occupied=rooms[index].occupied,
                price=rooms[index].price,
            )
            if room_model.occupied:
                room_model.occupant = occupant[index]
                room_model.guarantor = guarantor[index]
            roomInfoModel.append(room_model)

        return {'flag': True, 'data': roomInfoModel}

    def get_rent(self) -> int:
        price: int = 0

        for room_detail in room_number.values():
            price += room_detail[1]

        return {'flag': True, 'data': price}

    def get_room_rent(self, room_id) -> int:
        for room, room_detail in room_number.items():

            if room == room_id:
                return {'flag': True, 'data': room_detail[1]}

        return {'flag': False, 'message': 'Room not found'}

    def add_room(self):
        if len(self.get_all_rooms()) < 63:
            with Session(self.engine) as session:
                occupant = Occupant()
                session.add(occupant)

                guarantor = Guarantor()
                session.add(guarantor)

                session.commit()

                room = RoomInfo(roomNumber=room_number[occupant.id][0], occupied=False,
                                occupant_id=occupant.id, guarantor_id=guarantor.id, price=room_number[occupant.id][1])
                session.add(room)
                session.commit()
                session.refresh(room)
                return {'flag': True, 'data': RoomInfoModel(
                        id=occupant.id,
                        roomNumber=room_number[occupant.id][0],
                        price=room_number[occupant.id][1],
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
