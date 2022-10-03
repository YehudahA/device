

from models.door_status import DoorStatus
from models.content_status import ContentStatus


class BoxStatus():
    def __init__(self, content: ContentStatus, door: DoorStatus):
        self.content = content
        self.door = door

    def serialize(self):
        return {
            "content": self.content.name,
            "door": self.door.name
        }
