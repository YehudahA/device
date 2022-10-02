from dependency_injector import containers, providers
from services.fake_device_agent import FakeDeviceAgent
from services.mcu_service import MCUService


class Container(containers.DeclarativeContainer):
    device_agent = providers.Singleton(
        FakeDeviceAgent
    )
    
    mcu_service = providers.Singleton(
        MCUService,
        device_agent
    )
