"""

"""

import zmq
import json
import asyncio
import accessi_local as Access
from PySide6.QtCore import Signal, QObject
from shared_methods import convert_websocket_data_to_image, calculate_latency


class AccessiWebsocket(QObject):
    status_websocket_signal = Signal(str)

    def __init__(self, Access: Access, window):
        super().__init__()
        self.PUBLISH_PORT = None
        self.Access = Access
        self.window = window

    async def get_websocket_data(self, connected_event: asyncio.Event):
        async with await Access.connect_websocket() as websocket:
            connected_event.set()
            context = zmq.Context()
            publisher_socket = context.socket(zmq.PUB)
            self.PUBLISH_PORT = publisher_socket.bind_to_random_port("tcp://127.0.0.1")
            while True:
                try:
                    message = await websocket.recv()
                    decoded_message = json.dumps(Access.handle_websocket_message(message)).encode()
                    publisher_socket.send(decoded_message)
                    _, metadata = convert_websocket_data_to_image(decoded_message)
                    self.status_websocket_signal.emit(f"Latency: {calculate_latency(metadata)}s")
                except Exception as err:
                    if "received 1000 (OK); then sent 1000 (OK)" not in str(err):
                        print(f"Websocket error: {err}")

    async def main(self):
        try:
            # Run websocket
            websocket_connected_event = asyncio.Event()
            asyncio.create_task(self.get_websocket_data(connected_event=websocket_connected_event))
            await websocket_connected_event.wait()
            image_service = Access.Image.connect_to_default_web_socket()
            print(f"Access-i ImageServiceConnection: {image_service}")
            Access.Image.set_image_format("raw16bit")
            while self.window.ui.check_websocket_active.isChecked():
                await asyncio.sleep(0.05)
        except Exception as error:
            print("An error occurred:", error)

    def run_websocket_thread(self):
        try:
            asyncio.run(self.main())
        except Exception as error:
            print(error)
