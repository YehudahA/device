from models.box_status import BoxStatus
from models.door_status import DoorStatus
from models.content_status import ContentStatus

from threading import Timer


class Box:
    def __init__(self,
                 id: int,
                 content: ContentStatus,
                 door: DoorStatus
                 ) -> None:
        self.id = id
        self.content = content
        self.door = door


class FakeDataService:
    boxes = [
        Box(1, ContentStatus.FULL, DoorStatus.CLOSED),
        Box(2, ContentStatus.FULL, DoorStatus.OPEN),
        Box(3, ContentStatus.FULL, DoorStatus.CLOSED),
        Box(4, ContentStatus.FULL, DoorStatus.OPEN),
        Box(5, ContentStatus.EMPTY, DoorStatus.CLOSED),
        Box(6, ContentStatus.EMPTY, DoorStatus.OPEN),
        Box(7, ContentStatus.EMPTY, DoorStatus.CLOSED),
        Box(8, ContentStatus.EMPTY, DoorStatus.OPEN)
    ]

    def find(self, id: int):
        return next(filter(lambda b: b.id == id, self.boxes))

    def getStatus(self, id: int):
        box = self.find(id)
        return BoxStatus(box.content, box.door)

    def open(self, id: int):
        box = self.find(id)
        box.door = DoorStatus.OPEN

        def reopen():
            box.door = DoorStatus.CLOSED

        timer = Timer(10, reopen)
        timer.start()


class FakeDeviceAgent:
    buffer: bytearray

    def __init__(self) -> None:
        self.db = FakeDataService()

    def write(self, content: bytearray):
        boxId = content[8]

        if boxId == 255:
            line1 = bytearray([188, 203, 0, 0, 0, 1, 92])
            statuses = list(
                map(lambda b: FakeDeviceAgent.box_status(b), self.db.boxes))
            line2 = bytearray(statuses)
            self.buffer = line1 + line2

        else:
            box = self.db.find(boxId)
            status = FakeDeviceAgent.box_status(box)
            self.buffer = bytearray(
                [188, 203, 0, 0, 0, 1, 3, 160, boxId, status])

    def read(self, length: int) -> bytearray:
        len2 = length if length == 7 or length == 7 else len(self.buffer)
        arr = self.buffer[0:len2]
        self.buffer = self.buffer[len2:]
        return arr

    def box_status(box: Box) -> int:
        letter = 0 if box.content == ContentStatus.EMPTY else 16
        door = 0 if box.door == DoorStatus.CLOSED else 1
        return door + letter
