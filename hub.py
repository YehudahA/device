import websocket
import rel

def on_message(ws, message):
    print("New Message")
    print(message)

def on_error(ws, error):
    print(error)

def on_close(ws, close_status_code, close_msg):
    print("### closed ###")

def on_open(ws):
    print("Opened connection")

def init_socket():
    websocket.enableTrace(True)
    ws = websocket.WebSocketApp("wss://ws.postman-echo.com/raw",
                              on_open=on_open,
                              on_message=on_message,
                              on_error=on_error,
                              on_close=on_close)

    ws.run_forever(dispatcher=rel)  
    rel.signal(2, rel.abort)  # Keyboard Interrupt  
    rel.dispatch()
    return ws
    
if __name__ == "__main__":
    init_socket()    