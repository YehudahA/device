import imp
import serial
import logging

_logger = logging.getLogger(__name__)

class DeviceAgent:
    def __init__(self):
        self.__device = serial.Serial(port='/dev/ttyS0',
                                      baudrate=38400)

    def write(self, content: bytearray):
        _logger.debug(content)
        self.__device.write(content)

    def read(self, length: int) -> bytearray:
        data = self.__device.read(length)
        _logger.debug(data)
        
        return data
