from models.box_status import BoxStatus
from models.door_status import DoorStatus
from models.fill_status import FillStatus

from threading import Timer


class Box:
    def __init__(self,
                 id: int,
                 full: FillStatus,
                 door: DoorStatus
                 ) -> None:
        self.id = id
        self.full = full
        self.door = door


class FakeDataService:
    boxes = [
        Box(1, FillStatus.FULL, DoorStatus.CLOSED),
        Box(2, FillStatus.FULL, DoorStatus.OPEN),
        Box(3, FillStatus.FULL, DoorStatus.CLOSED),
        Box(4, FillStatus.FULL, DoorStatus.OPEN),
        Box(5, FillStatus.EMPTY, DoorStatus.CLOSED),
        Box(6, FillStatus.EMPTY, DoorStatus.OPEN),
        Box(7, FillStatus.EMPTY, DoorStatus.CLOSED),
        Box(8, FillStatus.EMPTY, DoorStatus.OPEN)
    ]

    def find(self, id: int):
        return next(filter(lambda b: b.id == id, self.boxes))

    def getStatus(self, id: int):
        box = self.find(id)
        return BoxStatus(box.full, box.door)

    def open(self, id: int):
        box = self.find(id)
        box.door = DoorStatus.OPEN

        def reopen():
            box.door = DoorStatus.CLOSED

        timer = Timer(10, reopen)
        timer.start()
