import asyncio
import logging
from models.box_status import BoxStatusHelper

from services.mcu_service import MCUService

_logger = logging.getLogger(__name__)


class ServerUpdate:

    def __init__(self, mcu: MCUService, domain: str):
        self.mcu = mcu
        self.domain = domain

    def update(self):
        import requests
        statuses = self.mcu.get_all_box_status()
        payload = BoxStatusHelper.serializeList(statuses)
        response = requests.post(
            f'https://{self.domain}/api/Agent/Status', json=payload)
        return response.status_code

    def run(self):
        async def periodic():
            while True:
                try:
                    _logger.debug('post statuses')
                    self.update()
                except Exception as e:
                    _logger.exception(e)

                await asyncio.sleep(3)

        loop = asyncio.get_event_loop()
        loop.create_task(periodic())

        loop.run_forever()
