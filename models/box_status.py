

from models.door_status import DoorStatus
from models.full_status import FullStatus


class BoxStatus():
    def __init__(self, full: FullStatus, door: DoorStatus):
        self.full = full
        self.door = door

    def serialize(self):
        return {
            "full": self.full.name,
            "door": self.door.name
        }
