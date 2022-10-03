from dependency_injector import containers, providers

from services.device_agent import DeviceAgent
#from services.fake_device_agent import FakeDeviceAgent
from services.mcu_service import MCUService


class Container(containers.DeclarativeContainer):
    device_agent = providers.Singleton(
        DeviceAgent
    )

    mcu_service = providers.Singleton(
        MCUService,
        device_agent
    )
