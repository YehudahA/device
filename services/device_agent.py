import serial


class DeviceAgent:
    def __init1__(self):
        self.__device = serial.Serial(port=222,
                                      baudrate=115200,
                                      parity=serial.PARITY_NONE,
                                      stopbits=serial.STOPBITS_ONE,
                                      bytesize=serial.EIGHTBITS,
                                      timeout=3)

    def write(self, content: bytearray):
        self.__device.write(content)

    def read(self, length: int) -> bytearray:
        return self.__device.read(length)
