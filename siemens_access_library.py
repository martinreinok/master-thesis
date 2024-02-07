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
    def __init__(self, ip_address, port=7787, protocol="https", timeout=2, ssl_verify=False, version="v2"):
        self.ip_address = ip_address
        self.port = port
        self.version = version
        self.websocket_port = 7788
        self.protocol = protocol
        self.base_url = f"{protocol}://{ip_address}:{port}/SRC/product/remote"
        self.base_url_version = f"{protocol}://{ip_address}:{port}/SRC/{self.version}/product"
        self.base_url_v2 = f"{protocol}://{ip_address}:{port}/SRC/v2/product"
        self.timeout = timeout
        self.ssl_verify = ssl_verify
        self.headers = {"Content-Type": "application/json"}
        self.session_id = None

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
        url = f"wss://{self.ip_address}:{self.websocket_port}/SRC?sessionId={session_id}"
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
                 informal_name="utwente"):
        """
        Response example:
         - "result": {"success":true,"reason":"ok","time":"20170608_143325.423"},
         - "sessionId":"26eb060c-553d-4c15-bf5b23cf29012763"
         - "privilegeLevel":"advanced"
        """
        url = f"{self.base_url_version}/authorization/register"
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
        reply = self.send_request(url, data)
        self.session_id = reply.sessionId
        return reply

    def set_image_format(self, value: Literal["dicom", "raw16bit"] = "raw16bit"):
        """
        Either "value": "dicom | raw16bit"
        Response example:
         - "result": {"success":true,"reason":"ok","time":"20170608_143325.423"}
        """
        url = f"{self.base_url_version}/image/setImageFormat"
        data = {"sessionId": self.session_id, "value": value}
        return self.send_request(url, data)

    def get_last_series_number(self):
        """
        Response example:
         - "result":{"success":true,"reason":"ok","time":"20170608T143325.423"},
         - "value":1
        """
        url = f"{self.base_url_version}/image/getLastSeriesNumber"
        data = {"sessionId": self.session_id}
        return self.send_request(url, data, request_type="GET")

    def connect_image_service_to_default_web_socket(self):
        """
        Response example:
         - "result":{"success":true,"reason":"ok","time":"20170608T143325.423"}
        """
        url = f"{self.base_url_version}/image/connectServiceToDefaultWebSocket"
        data = {"sessionId": self.session_id}
        return self.send_request(url, data)

    def get_configured_parameters(self):
        """
        Response example:
         - "result":{"success":true,"reason":"ok","time":"20170608T143325.423"},
         - "value":[{
            - "index":1,
            - "id":"26eb060c-553d-4c15-bf5b23cf29012763",
            - "label":"ABC",
            - "type":"ABC",
            - "unit":"ABC",
            - "ProtocolTag":"ABC"},
            - {"index":1,
            - "id":"26eb060c-553d-4c15-bf5b23cf29012763",
            - "label":"ABC",
            - "type":"ABC",
            - "unit":"ABC",
            - "ProtocolTag":"ABC"}]
        """
        url = f"{self.base_url_version}/parameter/configured/getConfiguredParameters"
        data = {"sessionId": self.session_id}
        return self.send_request(url, data, "GET")

    def get_slice_position_dcs(self):
        """
        Response example:
         - "result":{"success":true,"reason":"ok","time":"20170608T143325.423"},
         - "value":{"x":10.0,"y":10.0,"z":20.0}
        """
        url = f"{self.base_url_version}/parameter/standard/getSlicePositionDcs"
        data = {"sessionId": self.session_id}
        return self.send_request(url, data, "GET")

    def get_slice_position_pcs(self):
        """
        Response example:
         - "result":{"success":true,"reason":"ok","time":"20170608T143325.423"},
         - "value":{"sag":10.0,"cor":-10.0,"tra":-20.0}
        """
        url = f"{self.base_url_version}/parameter/standard/getSlicePositionPcs"
        data = {"sessionId": self.session_id}
        return self.send_request(url, data, "GET")

    def get_slice_orientation_dcs(self):
        """
        Response example:
         - "result":{"success":true,"reason":"ok","time":"20170608T143325.423"},
         - "normal":{"x":0,"y":0,"z":-1.0},
         - "phase":{"x":0,"y":-1.0,"z":0},
         - "read":{"x":-1.0,"y":0,"z":0}
        """
        url = f"{self.base_url_version}/parameter/standard/getSliceOrientationDcs"
        data = {"sessionId": self.session_id}
        return self.send_request(url, data, "GET")

    def get_slice_orientation_pcs(self):
        """
        Response example:
         - "result":{"success":true,"reason":"ok","time":"20170608T143325.423"},
         - "normal":{"sag":0,"cor":0,"tra":1.0},
         - "phase":{"sag":0,"cor":1.0,"tra":0},
         - "read":{"sag":-1.0,"cor":0,"tra":0}
        """
        url = f"{self.base_url_version}/parameter/standard/getSliceOrientationPcs"
        data = {"sessionId": self.session_id}
        return self.send_request(url, data, "GET")

    def get_slice_thickness(self):
        """
        Unit:mm
        Response example:
         - "result":{"success":true,"reason":"ok","time":"20170608T143325.423"},
         - "value":2.5
        """
        url = f"{self.base_url_version}/parameter/standard/getSliceThickness"
        data = {"sessionId": self.session_id}
        return self.send_request(url, data, "GET")

    def set_slice_thickness(self, value, allow_side_effects=True):
        """
        Unit:mm
        Response example:
         - "result":{"success":true,"reason":"ok","time":"20170608T143325.423"},
         - "valueSet":3.5
        """
        url = f"{self.base_url_version}/parameter/standard/setSliceThickness"
        data = {"sessionId": self.session_id, "value": value, "allowSideEffects": allow_side_effects}
        return self.send_request(url, data)

    def get_host_control_state(self):
        """
        Response example:
         - "result":{"success":true,"reason":"ok","time":"20170608T143325.423"},
         - "value":{
            - "hasControl":true,
            - "canRequestControl":false,
            - "canReleaseControl":true,
            - "cannotRequestControlReason":"clientInControl"}
        """
        url = f"{self.base_url_version}/hostControl/getState"
        data = {"sessionId": self.session_id}
        return self.send_request(url, data, "GET")

    def request_host_control(self):
        """
        Response example:
         - "result":{"success":true,"reason":"ok","time":"20170608T143325.423"}
        """
        url = f"{self.base_url_version}/hostControl/requestControl"
        data = {"sessionId": self.session_id}
        return self.send_request(url, data)

    def release_host_control(self):
        """
        Response example:
         - "result":{"success":true,"reason":"ok","time":"20170608T143325.423"}
        """
        url = f"{self.base_url_version}/hostControl/releaseControl"
        data = {"sessionId": self.session_id}
        return self.send_request(url, data)

    def get_templates(self):
        """
        Response example:
         - "result":{"success":true,"reason":"ok","time":"20170608T143325.423"},
         - "value":[
            - {"id":"26eb060c-553d-4c15-bf5b-23cf29012763","label":"Interactive Template 1","isInteractive":true},
            - {"id":"abeb060c-553d-4c15-bf5b23cf29012763","label":"T2 Template","isInteractive":false}]}
        """
        url = f"{self.base_url_version}/templateExecution/getTemplates"
        data = {"sessionId": self.session_id}
        return self.send_request(url, data, "GET")

    def get_templates_state(self):
        """
        Response example:
         - "result":{"success":true,"reason":"ok","time":"20170608T143325.423"},
         - "value":{
            - "runningTemplate":{
                - "isApplicable":true,
                - "isTemplate":true,
                - "isInteractive":true,
                - "id":"26eb060c-553d-4c15-bf5b-23cf29012763",
                - "label":"Interactive Template 1"},
            - "canStart":false,
            - "canStop":true,
            - "canPause":true,
            - "canContinue":false,
            - "executionState":"scanning"}}
        """
        url = f"{self.base_url_version}/templateExecution/getState"
        data = {"sessionId": self.session_id}
        return self.send_request(url, data, "GET")

    def start_template(self, template_id):
        """
        Response example:
         - "result":{"success":true,"reason":"ok","time":"20170608T143325.423"}
        """
        url = f"{self.base_url_version}/templateExecution/start"
        data = {"sessionId": self.session_id, "id": template_id}
        return self.send_request(url, data)

    def stop_template(self):
        """
        Response example:
         - "result":{"success":true,"reason":"ok","time":"20170608T143325.423"}
        """
        url = f"{self.base_url_version}/templateExecution/stop"
        data = {"sessionId": self.session_id}
        return self.send_request(url, data)

