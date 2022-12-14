import websocket
import rel
import logging

_logger = logging.getLogger(__name__)


def on_error(ws, error):
    _logger.exception(error)


def on_close(ws, close_status_code, close_msg):
    _logger.info("### closed ###")


def on_open(ws):
    _logger.info("Opened connection")


def init_ws(on_message, domain):
    websocket.enableTrace(True)
    ws = websocket.WebSocketApp(f'wss://{domain}/ws',
                                on_open=on_open,
                                on_message=on_message,
                                on_error=on_error,
                                on_close=on_close)

    ws.run_forever(dispatcher=rel)  # Set dispatcher to automatic reconnection
    return ws


if __name__ == "__main__":
    ws = init_ws('localhost:7123')
    print('initialized!')
    rel.signal(2, rel.abort)  # Keyboard Interrupt
    rel.dispatch()
