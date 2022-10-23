from services.device_agent import DeviceAgent
from services.fake_device_agent import FakeDeviceAgent
from services.mcu_service import MCUService


class Container():
    #device_agent = DeviceAgent()
    device_agent = FakeDeviceAgent()

    mcu_service = MCUService(device_agent)
