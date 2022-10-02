from services.fake_data_service import FakeDataService


class MCUService:
    def __init__(self) -> None:
        self.service = FakeDataService()

    def get_box_status(self, box: int):
        return self.service.getStatus(box)

    def open_door(self, box: int):
        self.service.open(box)
