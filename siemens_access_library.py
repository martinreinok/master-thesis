"""
This is a library written for Siemens Access-i websocket requests.
Briefly tested with Access-i simulator
"""
import requests
import websockets
import asyncio
import urllib3
from types import SimpleNamespace
import json
from typing import Literal
import ssl

# ! Disables HTTPS incorrect SSL warning. (Don't use in production unless aware of consequences)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class Access:
    def __init__(self, ip_address, port=7787, protocol="https", timeout=2, ssl_verify=False):
        self.ip_address = ip_address
        self.port = port
        self.websocket_port = 7788
        self.protocol = protocol
        self.base_url = f"{protocol}://{ip_address}:{port}/SRC/product/remote"
        self.base_url_v2 = f"{protocol}://{ip_address}:{port}/SRC/v2/product"
        self.timeout = timeout
        self.ssl_verify = ssl_verify
        self.headers = {"Content-Type": "application/json"}

    @staticmethod
    def response_to_object(json_response):
        return json.loads(json.dumps(json_response.json()), object_hook=lambda d: SimpleNamespace(**d))

    def send_request(self, url, data, request_type: Literal["GET", "POST"] = "POST"):
        if request_type == "GET":
            response = requests.get(url, headers=self.headers, json=data, timeout=self.timeout, verify=self.ssl_verify)
        elif request_type == "POST":
            response = requests.post(url, headers=self.headers, json=data, timeout=self.timeout, verify=self.ssl_verify)
        else:
            raise SystemExit(f"request type incorrect {request_type}")
        response.raise_for_status()
        return self.response_to_object(response)

    @staticmethod
    def handle_websocket_message(data):
        service, request, response, message = None, None, None, None
        try:
            message = json.loads(data)
            service = message.get('service', '')
            request = message.get('request', '')
            response = message.get('response', '')
            print("Service:", service)
            print("Request:", request)
            # print("Response:", response)
        except json.JSONDecodeError as e:
            print("Error decoding JSON:", e)
        return [service, request, response, message]

    async def connect_websocket(self, session_id, callback_function):
        url = f"wss://127.0.0.1:7788/SRC?sessionId={session_id}"
        ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
        ssl_context.check_hostname = True
        ssl_context.verify_mode = ssl.CERT_REQUIRED
        if not self.ssl_verify:
            ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
            ssl_context.check_hostname = False
            ssl_context.verify_mode = ssl.CERT_NONE
        async with websockets.connect(url, ssl=ssl_context) as websocket:
            while True:
                message = await websocket.recv()
                decoded_message = self.handle_websocket_message(message)
                await callback_function(decoded_message)

    def get_is_active(self):
        """
        Response example:
         - "result": {"success":true,"reason":"ok","time":"20170608_143325.423"},
         - "value":true,
         - "isProductionSystem":true
        """
        url = f"{self.base_url}/getIsActive"
        return self.send_request(url, data=None, request_type="GET")

    def get_version(self):
        """
        Response example:
         - "result": {"success":true,"reason":"ok","time":"20170608_143325.423"},
         - "value":"2.0"
        """
        url = f"{self.base_url}/getVersion"
        return self.send_request(url, data=None, request_type="GET")

    def register(self, name="Access_i SDK", comment=None, start_date="20180115", warn_date="20391215",
                 expire_date="20400115", system_id="99999999999999", is_read_option_available=True,
                 is_execute_option_available=True, is_advanced_option_available=True, version="1.0",
                 hash="drXXpUNoR8GVxi3GhXL2Gt3S7XSS8MPTyTM75ehUxnfIUBhmmPr%2BL2qTXWnS0csVoGiFoUZS1pVCteO3JxGO7A%3D%3D",
                 informal_name="Access-i Third Party Client"):
        """
        Response example:
         - "result": {"success":true,"reason":"ok","time":"20170608_143325.423"},
         - "sessionId":"26eb060c-553d-4c15-bf5b23cf29012763"
         - "privilegeLevel":"advanced"
        """
        url = f"{self.base_url_v2}/authorization/register"
        data = {"license": {
            "Name": name,
            "Comment": comment,
            "StartDate": start_date,
            "WarnDate": warn_date,
            "ExpireDate": expire_date,
            "SystemId": system_id,
            "IsReadOptionAvailable": is_read_option_available,
            "IsExecuteOptionAvailable": is_execute_option_available,
            "IsAdvancedOptionAvailable": is_advanced_option_available,
            "Version": version,
            "Hash": hash
        },
            "name": informal_name}
        return self.send_request(url, data)

    def set_image_format(self, session_id, value: Literal["dicom", "raw16bit"] = "raw16bit"):
        """
        Either "value": "dicom | raw16bit"
        Response example:
         - "result": {"success":true,"reason":"ok","time":"20170608_143325.423"}
        """
        url = f"{self.base_url_v2}/image/setImageFormat"
        data = {"sessionId": session_id, "value": value}
        return self.send_request(url, data)

    def get_last_series_number(self, session_id):
        """
        Response example:
         - "result":{"success":true,"reason":"ok","time":"20170608T143325.423"},
         - "value":1
        """
        url = f"{self.base_url_v2}/image/getLastSeriesNumber"
        data = {"sessionId": session_id}
        return self.send_request(url, data, request_type="GET")

    def connect_image_service_to_default_web_socket(self, session_id):
        """
        Response example:
         - "result":{"success":true,"reason":"ok","time":"20170608T143325.423"}
        """
        url = f"{self.base_url_v2}/image/connectServiceToDefaultWebSocket"
        data = {"sessionId": session_id}
        return self.send_request(url, data)


Access = Access("10.89.184.9")

active_check = Access.get_is_active()
if active_check is None:
    raise SystemExit("Server not active")
print(f"Active: {active_check.value}")

version = Access.get_version()
print(f"Version: {version.value}")

register = Access.register(name="UTwente", start_date="20231102", warn_date="20251002",
                           expire_date="20251102", system_id="152379",
                           hash="uTwo2ohlQvMNHhfrzceCRzfRSLYDAw7zqojGjlP%2BCEmqPq1IxUoyx5hOGYbiO%2FEIyiaA4oFHFB2fwTctDbRWew%3D%3D")
print(f"Register: {register.result.success}, Session: {register.sessionId}")

image_format = Access.set_image_format(register.sessionId, "raw16bit")

"""
Initialize websocket loop for image service
"""
# Connect the image service to existing websocket

image_service = Access.connect_image_service_to_default_web_socket(register.sessionId)
print(f"ImageServiceConnection: {image_service.result.success}")
