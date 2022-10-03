from flask import Flask, jsonify
from container import Container
from dependency_injector.wiring import Provide, inject
import logging
import logging.handlers as handlers
import os
from sys import platform

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


def configLogging():
    logLevelArg = logging.DEBUG

    consoleLogLevel, fileLogLevel = logLevelArg, logLevelArg

    if not logLevelArg:
        consoleLogLevel, fileLogLevel = logging.INFO, logging.WARNING
        
    logging.basicConfig(level=consoleLogLevel, format='%(levelname)s|%(name)s|%(message)s')

    logs_dir = "C:/Logs/pyAgent" if platform == "win32" else "/home/ipis/logs"
     
    if not os.path.isdir(logs_dir):
        os.mkdir(logs_dir, mode=0o777)
        os.chmod(logs_dir, 0o777)
        
    fileHandler = handlers.TimedRotatingFileHandler(logs_dir + '/pyagent_app.log', when='MIDNIGHT', backupCount=7)
    fileHandler.setLevel(fileLogLevel)
    fileHandler.setFormatter(logging.Formatter('%(asctime)s|%(levelname)s|%(filename)s:%(lineno)d|%(message)s'))
    logging.root.addHandler(fileHandler)

if __name__ == "__main__":
    container = Container()
    container.wire(modules=[__name__])
    create_app().run()
