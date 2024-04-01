"""
This is a library written for Siemens Access-i websocket requests.
Only insecure HTTPS is currently supported.
"""
# TODO: TemplateSelection Service Not implemented.
# TODO: Patient Service Not implemented.
# TODO: Parameter Standard Service partially implemented.
# TODO: Table Service Not implemented.
# TODO: Tracking Service Not implemented.
# TODO: Issue Service Not implemented.
# TODO: Adjustment Service Not implemented.
# TODO: Debugging Service Not implemented.

from types import SimpleNamespace
from typing import Literal
import numpy as np
import websockets
import requests
import urllib3
import asyncio
import json
import ssl

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class config:
    """
    User-configurable variables for establishing a connection with the MR host.
    IP-address is None by default (localhost ip is 127.0.0.1)
    """
    ip_address = None
    port = 7787
    version = "v2"
    websocket_port = 7788
    protocol = "https"
    session_id = None
    ssl_verify = False
    timeout = 2
    headers = {"Content-Type": "application/json"}

    @staticmethod
    def base_url():
        return f"{config.protocol}://{config.ip_address}:{config.port}/SRC/{config.version}/product"

    @staticmethod
    def base_url_remote():
        return f"{config.protocol}://{config.ip_address}:{config.port}/SRC/product/remote"

    @staticmethod
    def websocket_default_url():
        return f"wss://{config.ip_address}:{config.websocket_port}/SRC?sessionId={config.session_id}"


class Remote:
    """
    The remote service provides the RC with options to check whether and which version of the SRC is up and running
    on the MR host. This service requires no prior authorization of the RC.
    """

    @staticmethod
    def get_is_active():
        """
        Response example:
         - "result": {"success":true,"reason":"ok","time":"20170608_143325.423"},
         - "value":true,
         - "isProductionSystem":true
        """
        url = f"{config.base_url_remote()}/getIsActive"
        return send_request(url, data=None, request_type="GET")

    @staticmethod
    def get_version():
        """
        Response example:
         - "result": {"success":true,"reason":"ok","time":"20170608_143325.423"},
         - "value":"2.0"
        """
        url = f"{config.base_url_remote()}/getVersion"
        return send_request(url, data=None, request_type="GET")


class Authorization:
    """
    The Authorization service (authorization) ensures that only RCs with a valid authentication key
    can communicate with the Access-i server.
    Before any of the services described in this document can be used,
    an RC must register providing a valid authentication key (provided by your point of contact at Siemens Healthineers),
    which also encodes the scope of functionality that can be used by the RC.
    """

    @staticmethod
    def register(name="Access_i SDK", comment=None, start_date="20180115", warn_date="20391215",
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
        url = f"{config.base_url()}/authorization/register"
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
        reply = send_request(url, data, request_type="POST")
        config.session_id = reply.sessionId
        return reply

    @staticmethod
    def get_is_registered():
        """
        Response example:
         - result":{"success":true,"reason":"ok","time":"20170608T143325.423"},
         - "value":true,
         - "privilegeLevel":"advanced"
        """
        url = f"{config.base_url()}/authorization/getIsRegistered"
        data = {"sessionId": config.session_id}
        return send_request(url, data=data, request_type="GET")

    @staticmethod
    def deregister():
        """
        Response example:
         - result":{"success":true,"reason":"ok","time":"20170608T143325.423"}
        """
        url = f"{config.base_url()}/authorization/deregister"
        data = {"sessionId": config.session_id}
        return send_request(url, data=data, request_type="POST")


class HostControl:
    """
    The Host Control Service allows changing the entity that is controlling
    the MR host which is either the MR host itself or an RC.
    At a given point in time only one entity can actively control the host, i.e.
    has the mastership with respect to controlling the workflow.
    As soon as an RC releases the control, the MR host is automatically in charge.
    The RC can only retrieve the mastership if a patient is registered and no sequence is running or open.
    """

    @staticmethod
    def get_state():
        """
        Response example:
         - "result":{"success":true,"reason":"ok","time":"20170608T143325.423"},
         - "value":{
            - "hasControl":true,
            - "canRequestControl":false,
            - "canReleaseControl":true,
            - "cannotRequestControlReason":"clientInControl"}
        """
        url = f"{config.base_url()}/hostControl/getState"
        data = {"sessionId": config.session_id}
        return send_request(url, data=data, request_type="GET")

    @staticmethod
    def request_host_control():
        """
        Response example:
         - "result":{"success":true,"reason":"ok","time":"20170608T143325.423"}
        """
        url = f"{config.base_url()}/hostControl/requestControl"
        data = {"sessionId": config.session_id}
        return send_request(url, data, request_type="POST")

    @staticmethod
    def release_host_control():
        """
        Response example:
         - "result":{"success":true,"reason":"ok","time":"20170608T143325.423"}
        """
        url = f"{config.base_url()}/hostControl/releaseControl"
        data = {"sessionId": config.session_id}
        return send_request(url, data, request_type="POST")


class SystemInformation:
    """
    The System Information Service provides general information about the MR scanner.
    Furthermore, it provides a standardized IsoCenter position to let a Remote Client know where the system laser
    has been positioned.
    """

    @staticmethod
    def get_system_info():
        """
        Response example:
         - "result":{"success":true,"reason":"ok","time":"20170608T143325.423"},
         - "value":{
            - "systemModel":"Aera",
            - "fieldStrength":"1.5",
            - "gradientType":"XJ",
            - "numberOfRxChannels":48,
            - "softwareVersion":"N4_VE11C_LATEST_20160120"}
        """
        url = f"{config.base_url()}/systemInformation/getSystemInfo"
        data = {"sessionId": config.session_id}
        return send_request(url, data, request_type="GET")

    @staticmethod
    def get_isocenter_position():
        """
        Response example:
         - "result":{"success":true,"reason":"ok","time":"20170608T143325.423"},
         - "isDefined":true,
         - "value":132
        """
        url = f"{config.base_url()}/systemInformation/getIsocenterPosition"
        data = {"sessionId": config.session_id}
        return send_request(url, data, request_type="GET")

    @staticmethod
    def get_handball_state():
        """
        Response example:
         - "result":{"success":true,"reason":"ok","time":"20170608T143325.423"},
         - "value":"idle"
        """
        url = f"{config.base_url()}/systemInformation/getHandballState"
        data = {"sessionId": config.session_id}
        return send_request(url, data, request_type="GET")

    @staticmethod
    def get_serial_number():
        """
        Response example:
         - "result":{"success":true,"reason":"ok","time":"20170608T143325.423"},
         - "value":"12345"
        """
        url = f"{config.base_url()}/systemInformation/getSerialNumber"
        data = {"sessionId": config.session_id}
        return send_request(url, data, request_type="GET")


class TemplateExecution:
    """
    The Template Execution Service (templateExecution) allows retrieving all templates that can be remotely executed,
    i.e. that are currently loaded in the queue.
    The controlling RC may start, stop, pause and continue a template and retrieve the
    remaining measurement of the currently running template.

    NOTE: The RC is always able to stop a running sequence, also when it is not in control.
    """

    @staticmethod
    def get_templates():
        """
        Response example:
         - "result":{"success":true,"reason":"ok","time":"20170608T143325.423"},
         - "value":[
            - {"id":"26eb060c-553d-4c15-bf5b-23cf29012763","label":"Interactive Template 1","isInteractive":true},
            - {"id":"abeb060c-553d-4c15-bf5b23cf29012763","label":"T2 Template","isInteractive":false}]}
        """
        url = f"{config.base_url()}/templateExecution/getTemplates"
        data = {"sessionId": config.session_id}
        return send_request(url, data, "GET")

    @staticmethod
    def get_state():
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
        url = f"{config.base_url()}/templateExecution/getState"
        data = {"sessionId": config.session_id}
        return send_request(url, data, "GET")

    @staticmethod
    def get_remaining_measurement_time_in_seconds():
        """
        Response example:
         - "result":{"success":true,"reason":"ok","time":"20170608T143325.423"},
         - "isApplicable":true,
         - "value":15.5
        """
        url = f"{config.base_url()}/templateExecution/getRemainingMeasurementTimeInSeconds"
        data = {"sessionId": config.session_id}
        return send_request(url, data, "GET")

    @staticmethod
    def start(template_id):
        """
        Response example:
         - "result":{"success":true,"reason":"ok","time":"20170608T143325.423"}
        """
        url = f"{config.base_url()}/templateExecution/start"
        data = {"sessionId": config.session_id, "id": template_id}
        return send_request(url, data, "POST")

    @staticmethod
    def stop():
        """
        Response example:
         - "result":{"success":true,"reason":"ok","time":"20170608T143325.423"}
        """
        url = f"{config.base_url()}/templateExecution/stop"
        data = {"sessionId": config.session_id}
        return send_request(url, data, "POST")

    @staticmethod
    def pause():
        """
        Response example:
         - "result":{"success":true,"reason":"ok","time":"20170608T143325.423"}
        """
        url = f"{config.base_url()}/templateExecution/pause"
        data = {"sessionId": config.session_id}
        return send_request(url, data, "POST")

    @staticmethod
    def continue_():
        """
        Response example:
         - "result":{"success":true,"reason":"ok","time":"20170608T143325.423"}
        """
        url = f"{config.base_url()}/templateExecution/continue"
        data = {"sessionId": config.session_id}
        return send_request(url, data, "POST")


class TemplateModification:
    """
    The Template Modification Service (templateModification) allows opening and closing of templates in the queue and
    saving changes of template parameters (close with parameter 'saveChanges' == true).
    Template parameters may only be changed or queried while the template is open using the Parameter Service.
    """

    @staticmethod
    def get_state():
        """
        Response example:
         - "result":{"success":true,"reason":"ok","time":"20170608T143325.423"},
         - "value":{
            - "openTemplate":{
                - "isApplicable":true,
                - "isTemplate":true,
                - "isInteractive" :true,
                - "id":"26eb060c-553d-4c15-bf5b-23cf29012763",
                - "label":"Interactive Template 1"},
            - "canOpen":false,
            - "canClose":true}
        """
        url = f"{config.base_url()}/templateModification/getState"
        data = {"sessionId": config.session_id}
        return send_request(url, data, "GET")

    @staticmethod
    def open(template_id):
        """
        Response example:
         - "result":{"success":true,"reason":"ok","time":"20170608T143325.423"}
        """
        url = f"{config.base_url()}/templateModification/open"
        data = {"sessionId": config.session_id, "id": template_id}
        return send_request(url, data, "POST")

    @staticmethod
    def close(save_changes: bool = False):
        """
        Response example:
         - "result":{"success":true,"reason":"ok","time":"20170608T143325.423"}
        """
        url = f"{config.base_url()}/templateModification/close"
        data = {"sessionId": config.session_id, "saveChanges": save_changes}
        return send_request(url, data, "POST")


class ParameterStandard:
    """
    The Standard Parameter Service (parameter/standard) allows remote access to the protocol parameters of a
    template that is currently open in the program queue at the scanner.
    This includes reading and writing several protocol parameters like acquisition order, positioning mode,
    slice group position and orientation, base resolution and more.

    NOTE: Only some of the methods have been implemented.
    The full list of implementable parameters is in Access-i Dev Guide document.

    PCS: Patient Coordinate System (Not implemented)
    DCS: Device Coordinate System
    """

    @staticmethod
    def get_slice_position_dcs():
        """
        Response example:
         - "result":{"success":true,"reason":"ok","time":"20170608T143325.423"},
         - "value":{"x":10.0,"y":10.0,"z":20.0}
        """
        url = f"{config.base_url()}/parameter/standard/getSlicePositionDcs"
        data = {"sessionId": config.session_id}
        return send_request(url, data, "GET")

    @staticmethod
    def set_slice_position_dcs(x=None, y=None, z=None, allow_side_effects=True, index=0):
        """
        Response example:
         - "result":{"success":true,"reason":"ok","time":"20170608T143325.423"},
         - "valueSet":{"x":10.0,"y":-10.0,"z":-20.0}
        """
        url = f"{config.base_url()}/parameter/standard/setSlicePositionDcs"
        data = {"sessionId": config.session_id,
                "index": index,
                "value": {"x": x, "y": y, "z": z},
                "allowSideEffects": allow_side_effects}
        return send_request(url, data, "POST")

    @staticmethod
    def get_slice_orientation_dcs():
        """
        Response example:
         - "result":{"success":true,"reason":"ok","time":"20170608T143325.423"},
         - "normal":{"x":0,"y":0,"z":-1.0},
         - "phase":{"x":0,"y":-1.0,"z":0},
         - "read":{"x":-1.0,"y":0,"z":0}
        """
        url = f"{config.base_url()}/parameter/standard/getSliceOrientationDcs"
        data = {"sessionId": config.session_id}
        return send_request(url, data, "GET")

    @staticmethod
    def set_slice_orientation_dcs(normal: tuple = (0, 0, 0), phase: tuple = (0, 0, 0), read: tuple = (0, 0, 0),
                                  allow_side_effects=True, index=0):
        """
        Response example:
         - "result":{"success":true,"reason":"ok","time":"20170608T143325.423"},
         - "normalSet":{"x":0,"y":0,"z":-1.0},
         - "phaseSet":{"x":0,"y":-1.0,"z":0},
         - "readSet":{"x":-1.0,"y":0,"z":0}
        """
        url = f"{config.base_url()}/parameter/standard/setSliceOrientationDcs"
        data = {"sessionId": config.session_id,
                "index": index,
                "normal": {"x": normal[0], "y": normal[1], "z": normal[2]},
                "phase": {"x": phase[0], "y": phase[1], "z": phase[2]},
                "read": {"x": read[0], "y": read[1], "z": read[2]},
                "allowSideEffects": allow_side_effects}
        return send_request(url, data, "POST")

    @staticmethod
    def set_slice_orientation_degrees(x_deg, y_deg, z_deg, allow_side_effects=True, index=0):
        """
        Response example:
         - "result":{"success":true,"reason":"ok","time":"20170608T143325.423"},
         - "normalSet":{"x":0,"y":0,"z":-1.0},
         - "phaseSet":{"x":0,"y":-1.0,"z":0},
         - "readSet":{"x":-1.0,"y":0,"z":0}
         Don't really understand how the math works
        """
        # Convert degrees to radians
        x_rad = np.radians(x_deg)
        y_rad = np.radians(y_deg)
        z_rad = np.radians(z_deg)

        # Calculate the rotation matrices around each axis
        Rx = np.array([[1, 0, 0], [0, np.cos(x_rad), -np.sin(x_rad)], [0, np.sin(x_rad), np.cos(x_rad)]])
        Ry = np.array([[np.cos(y_rad), 0, np.sin(y_rad)], [0, 1, 0], [-np.sin(y_rad), 0, np.cos(y_rad)]])
        Rz = np.array([[np.cos(z_rad), -np.sin(z_rad), 0], [np.sin(z_rad), np.cos(z_rad), 0], [0, 0, 1]])

        # Combine the rotation matrices to get the overall rotation matrix
        R = np.dot(Rz, np.dot(Ry, Rx))

        # Extract the orientation vectors (normal, phase, read) from the rotation matrix
        normal = R[:, 2]  # Third column
        phase = R[:, 1]  # Second column
        read = R[:, 0]  # First column

        # Normalize the vectors
        normal /= np.linalg.norm(normal)
        phase /= np.linalg.norm(phase)
        read /= np.linalg.norm(read)
        return ParameterStandard.set_slice_orientation_dcs(normal, phase, read, allow_side_effects, index)

    @staticmethod
    def get_slice_thickness():
        """
        Unit:mm
        Response example:
         - "result":{"success":true,"reason":"ok","time":"20170608T143325.423"},
         - "value":2.5
        """
        url = f"{config.base_url()}/parameter/standard/getSliceThickness"
        data = {"sessionId": config.session_id}
        return send_request(url, data, "GET")

    @staticmethod
    def get_field_of_view_read():
        """
        Unit:mm
        Response example:
         - "result":{"success":true,"reason":"ok","time":"20170608T143325.423"},
         - "value": 400.0
        """
        url = f"{config.base_url()}/parameter/standard/getFieldOfViewRead"
        data = {"sessionId": config.session_id}
        return send_request(url, data, "GET")

    @staticmethod
    def set_slice_thickness(value, allow_side_effects=True):
        """
        Unit:mm
        Response example:
         - "result":{"success":true,"reason":"ok","time":"20170608T143325.423"},
         - "valueSet":3.5
        """
        url = f"{config.base_url()}/parameter/standard/setSliceThickness"
        data = {"sessionId": config.session_id, "value": float(value), "allowSideEffects": allow_side_effects}
        return send_request(url, data, "POST")

    @staticmethod
    def get_base_resolution():
        """
        Unit:mm
        Response example:
         - "result":{"success":true,"reason":"ok","time":"20170608T143325.423"},
         - "value":128
        """
        url = f"{config.base_url()}/parameter/standard/getBaseResolution"
        data = {"sessionId": config.session_id}
        return send_request(url, data, "GET")

    @staticmethod
    def set_base_resolution(value, allow_side_effects=True):
        """
        Unit:mm
        Response example:
         - "result":{"success":true,"reason":"ok","time":"20170608T143325.423"},
         - "valueSet":192
        """
        url = f"{config.base_url()}/parameter/standard/setBaseResolution"
        data = {"sessionId": config.session_id, "value": value, "allowSideEffects": allow_side_effects}
        return send_request(url, data, "POST")


class Image:
    """
    Via the websocket functionality the client can automatically receive images that are reconstructed on the MR host.
    """

    @staticmethod
    def set_image_format(value: Literal["dicom", "raw16bit"] = "raw16bit"):
        """
        Response example:
         - "result": {"success":true,"reason":"ok","time":"20170608_143325.423"}
        """
        url = f"{config.base_url()}/image/setImageFormat"
        data = {"sessionId": config.session_id, "value": value}
        return send_request(url, data, "POST")

    @staticmethod
    def get_last_series_number():
        """
        Response example:
         - "result":{"success":true,"reason":"ok","time":"20170608T143325.423"},
         - "value":1
        """
        url = f"{config.base_url()}/image/getLastSeriesNumber"
        data = {"sessionId": config.session_id}
        return send_request(url, data, "GET")

    @staticmethod
    def connect_to_default_web_socket():
        """
        Response example:
         - "result": {"success":true,"reason":"ok","time":"20170608_143325.423"}
        """
        url = f"{config.base_url()}/image/connectServiceToDefaultWebSocket"
        data = {"sessionId": config.session_id}
        return send_request(url, data, "POST")


class ParameterConfigured:
    """
    The Configured Parameter Service (parameter/configured) allows the remote access to the protocol parameters
    of a protocol step that have been configured in the configurable parameter card within the AddIn of a template step.
    """

    @staticmethod
    def get_configured_parameters():
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
        url = f"{config.base_url()}/parameter/configured/getConfiguredParameters"
        data = {"sessionId": config.session_id}
        return send_request(url, data, "GET")

    @staticmethod
    def get_parameter_info(protocol_tag=None):
        """
        Response example:
         - "result":{"success":true,"reason":"ok","time":"20170608T143325.423"},
         - "id":{
            - "index":1,
            - "id":"26eb060c-553d-4c15-bf5b23cf29012763",
            - "label":"ABC",
            - "type":"ABC",
            - "unit":"ABC",
            - "ProtocolTag":"ABC"}
        """
        url = f"{config.base_url()}/parameter/configured/getParameterInfo"
        data = {"sessionId": config.session_id, "protocolTag": protocol_tag}
        return send_request(url, data, "GET")

    @staticmethod
    def get_parameter_value(parameter_id=None):
        """
        Response example:
         - "result":{"success":true,"reason":"ok","time":"20170608T143325.423"},
         - "value":"xyz"
        """
        url = f"{config.base_url()}/parameter/configured/getParameterValue"
        data = {"sessionId": config.session_id, "id": parameter_id}
        return send_request(url, data, "GET")

    @staticmethod
    def get_parameter_description(parameter_id=None):
        """
        Response example:
         - "result":{"success":true,"reason":"ok","time":"20170608T143325.423"},
         - "value":"ABC"
        """
        url = f"{config.base_url()}/parameter/configured/getParameterDescription"
        data = {"sessionId": config.session_id, "id": parameter_id}
        return send_request(url, data, "GET")

    @staticmethod
    def get_parameter_choices(parameter_id=None):
        """
        Response example:
         - "result":{"success":true,"reason":"ok","time":"20170608T143325.423"},
         - "value":["ABC","ABC"]
        """
        url = f"{config.base_url()}/parameter/configured/getParameterChoices"
        data = {"sessionId": config.session_id, "id": parameter_id}
        return send_request(url, data, "GET")

    @staticmethod
    def set_parameter_value(parameter_id=None, value=None, allow_side_effects=True):
        """
        Response example:
         - "result":{"success":true,"reason":"ok","time":"20170608T143325.423"},
         - "valueSet":"xyz"
        """
        url = f"{config.base_url()}/parameter/configured/setParameterValue"
        data = {"sessionId": config.session_id, "id": parameter_id, "value": value,
                "allowSideEffects": allow_side_effects}
        return send_request(url, data, "POST")

    @staticmethod
    def get_is_parameter_available(parameter_id=None):
        """
        Response example:
         - "result":{"success":true,"reason":"ok","time":"20170608T143325.423"},
         - "value":true
        """
        url = f"{config.base_url()}/parameter/configured/getIsParameterAvailable"
        data = {"sessionId": config.session_id, "id": parameter_id}
        return send_request(url, data, "GET")

    @staticmethod
    def get_is_parameter_editable(parameter_id=None):
        """
        Response example:
         - "result":{"success":true,"reason":"ok","time":"20170608T143325.423"},
         - "value":true
        """
        url = f"{config.base_url()}/parameter/configured/getIsParameterEditable"
        data = {"sessionId": config.session_id, "id": parameter_id}
        return send_request(url, data, "GET")

    @staticmethod
    def get_parameter_limits(parameter_id=None):
        """
        Response example:
         - "result":{"success":true,"reason":"ok","time":"20170608T143325.423"},
         - "value":[
         - {"min":1.0,"max":1.0,"increment":1.0,"restriction":"ABC","interval":"ABC"},
         - {"min":1.0,"max":1.0,"increment":1.0,"restriction":"ABC","interval": "ABC"}]
        """
        url = f"{config.base_url()}/parameter/configured/getParameterLimits"
        data = {"sessionId": config.session_id, "id": parameter_id}
        return send_request(url, data, "GET")


def handle_websocket_message(data):
    service, request, response, message = None, None, None, None
    try:
        message = json.loads(data)
        service = message.get('service', '')
        request = message.get('request', '')
        response = message.get('response', '')
    except json.JSONDecodeError as e:
        print("Error decoding JSON:", e)
    return [service, request, response, message]


async def connect_websocket():
    """
    Connects to the websocket server and returns the connected websocket object.
    Returns websockets.legacy.client.Connect object
    """
    try:
        url = config.websocket_default_url()
        if not config.ssl_verify:
            ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
            ssl_context.check_hostname = False
            ssl_context.verify_mode = ssl.CERT_NONE
        else:
            raise SystemExit("SSL verification not supported yet")
        return websockets.connect(url, ssl=ssl_context)
    except (websockets.ConnectionClosed, asyncio.TimeoutError) as e:
        raise ConnectionError("Connection failed: " + str(e)) from e
    except Exception as e:
        raise e


def response_to_object(json_response):
    return json.loads(json.dumps(json_response.json()), object_hook=lambda d: SimpleNamespace(**d))


def send_request(url, data, request_type: Literal["GET", "POST"] = "POST"):
    if request_type == "GET":
        response = requests.get(url, headers=config.headers, json=data, timeout=config.timeout,
                                verify=config.ssl_verify)
    elif request_type == "POST":
        response = requests.post(url, headers=config.headers, json=data, timeout=config.timeout,
                                 verify=config.ssl_verify)
    else:
        raise SystemExit(f"request type incorrect {request_type}")
    response.raise_for_status()
    return response_to_object(response)
