

from models.door_status import DoorStatus
from models.fill_status import FillStatus


class BoxStatus():
    def __init__(self, full: FillStatus, door: DoorStatus):
        self.full = full
        self.door = door

    def serialize(self):
        return {
            "full": self.full.name,
            "door": self.door.name
        }
