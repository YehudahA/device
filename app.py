from flask import Flask, jsonify
from container import Container
from dependency_injector.wiring import Provide, inject

from services.mcu_service import MCUService


@inject
def get_box_status(id: int, service: MCUService = Provide[Container.mcu_service]):
    box = service.get_box_status(id)
    return box[0].serialize()

@inject
def get_all_statuses(service: MCUService = Provide[Container.mcu_service]):
    boxes = service.get_box_status(255)
    return jsonify(list(map(lambda b: b.serialize(), boxes)))

@inject
def open_box(id: int, service: MCUService = Provide[Container.mcu_service]):
    service.open_door(id)
    return ('', 204)


def create_app() -> Flask:
    app = Flask(__name__)
    app.add_url_rule("/status/all", "all", get_all_statuses, methods=['GET'])
    app.add_url_rule("/status/<int:id>", "status", get_box_status, methods=['GET'])
    app.add_url_rule("/open/<int:id>", "open", open_box, methods=['GET'])

    return app


if __name__ == "__main__":
    container = Container()
    container.wire(modules=[__name__])
    create_app().run()
