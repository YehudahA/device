from models.box_status import BoxStatus
from models.door_status import DoorStatus
from models.full_status import FullStatus
from services.device_agent import DeviceAgent
from enum import Enum


class Command(Enum):
    OPEN = 1
    GET_STATUS = 2
    CHANGE_DISPLAY = 3


class MCUService:
    box_count = 8

    def __init__(self, device: DeviceAgent):
        self.__service = device

    def get_box_status(self, box: int):
        cmd = MCUService.build_command(Command.GET_STATUS, box)
        self.__service.write(cmd)

        result0 = self.__service.read(7)
        length = result0[6]
        status_bytes = self.__service.read(
            length)[2:3] if length != 92 else self.__service.read(length)

        return list(map(lambda i: MCUService.int_to_box_status(i), status_bytes))

    def open_door(self, box: int):
        cmd = MCUService.build_command(Command.OPEN, box)
        self.__service.write(cmd)

    def build_command(command: Command, box: int = 255):
        return bytearray([188, 203, 0, 0, 0, 1, 3, 160 + command.value, box, 0])

    def int_to_box_status(i: int):
        bools = MCUService.int_to_bools(i)
        return BoxStatus(FullStatus.FULL if bools[0] else FullStatus.EMPTY, DoorStatus.OPEN if bools[1] else DoorStatus.CLOSED)

    def int_to_bools(i: int):
        formatted = "{:02x}".format(i)
        return list(map(lambda b: b == '1', formatted))
