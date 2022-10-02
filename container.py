from dependency_injector import containers, providers
from services.mcu_service import MCUService


class Container(containers.DeclarativeContainer):
    mcu_service = providers.Singleton(
        MCUService
    )
