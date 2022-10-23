import rel
from flask import Flask, jsonify
from flask_cors import CORS
from multiprocessing import Process
from container import Container
import logging
import logging.handlers as handlers
import os
from sys import platform
from hub import init_ws

from services.mcu_service import MCUService

container = Container()
mcu = container.mcu_service

def get_box_status(id: int):
    box = mcu.get_box_status(id)
    return box[0].serialize()


def get_all_statuses():
    boxes = mcu.get_box_status(255)
    return jsonify(list(map(lambda b: b.serialize(), boxes)))


def open_box(id: int):
    mcu.open_door(id)
    return ('', 204)

def create_app() -> Flask:
    app = Flask(__name__)
    app.add_url_rule("/status/all", "all", get_all_statuses, methods=['GET'])
    app.add_url_rule("/status/<int:id>", "status",
                     get_box_status, methods=['GET'])
    app.add_url_rule("/open/<int:id>", "open",
                     open_box, methods=['GET', 'POST'])

    cors = CORS(app)

    return app


def configLogging():
    logLevelArg = logging.DEBUG

    consoleLogLevel, fileLogLevel = logLevelArg, logLevelArg

    if not logLevelArg:
        consoleLogLevel, fileLogLevel = logging.INFO, logging.WARNING

    logging.basicConfig(level=consoleLogLevel,
                        format='%(levelname)s|%(name)s|%(message)s')

    logs_dir = "C:/Logs/pyAgent" if platform == "win32" else "/home/ipis/logs"

    if not os.path.isdir(logs_dir):
        os.mkdir(logs_dir, mode=0o777)
        os.chmod(logs_dir, 0o777)

    fileHandler = handlers.TimedRotatingFileHandler(
        logs_dir + '/pyagent_app.log', when='MIDNIGHT', backupCount=7)
    fileHandler.setLevel(fileLogLevel)
    fileHandler.setFormatter(logging.Formatter(
        '%(asctime)s|%(levelname)s|%(filename)s:%(lineno)d|%(message)s'))
    logging.root.addHandler(fileHandler)

def run_app():
    app = create_app()
    app.run()

def open_box_from_server(ws, msg: str):
    import re
    m = re.search('OPEN (\d+)', msg)

    if m:
        box = int(m.group(1))
        mcu.open_door(box)


if __name__ == "__main__":        
    appsthread = Process(target=run_app)
    appsthread.start()
    print('app initialized')
    
    ws = init_ws(open_box_from_server)
    print('socket initialized')

    rel.signal(2, rel.abort)  # Keyboard Interrupt
    rel.dispatch()

    appsthread.terminate()
