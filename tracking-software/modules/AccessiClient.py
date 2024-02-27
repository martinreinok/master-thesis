from PySide6.QtWidgets import QTableWidgetItem
import accessi_local as Access


class AccessiClient:

    def __init__(self, ui):
        self.ui = ui
        self.Access = Access
        self.template_id = None
        self.registered = False

    def register(self):
        ip_address = self.ui.field_ip_address.text()
        client_name = self.ui.field_client_name.text()
        version = self.ui.field_version.text()
        self.ui.status_register.setText("")
        self.ui.status_request_control.setText("")
        self.ui.status_release_control.setText("")
        if all(field is not None for field in [ip_address, client_name, version]):
            self.Access.config.ip_address = self.ui.field_ip_address.text()
            self.Access.config.version = version
            self.Access.config.timeout = 8
            try:
                reg = self.Access.Authorization.register(name="UTwente", start_date="20231102", warn_date="20251002",
                                                         expire_date="20251102", system_id="152379",
                                                         hash="uTwo2ohlQvMNHhfrzceCRzfRSLYDAw7zqojGjlP%2BCEmqPq1IxUoyx5hOGYbiO%2FEIyiaA4oFHFB2fwTctDbRWew%3D%3D",
                                                         informal_name=client_name)
            except Exception as error:
                self.ui.status_register.setStyleSheet("color: red")
                self.ui.status_register.setText(str(error))
                return
            if reg.result.success:
                self.ui.status_register.setStyleSheet("color: green")
                self.ui.status_register.setText(f"{reg.result.success}, privilege: {reg.privilegeLevel}")
                self.ui.button_request_control.setEnabled(True)
                self.ui.button_get_templates.setEnabled(True)
                self.ui.button_get_parameter.setEnabled(True)
                self.ui.button_set_parameter.setEnabled(True)
                self.ui.check_websocket_active.setEnabled(True)
                self.ui.check_websocket_active.stateChanged.emit(self.ui.check_websocket_active.isChecked())
                self.registered = True
            else:
                self.ui.status_register.setStyleSheet("color: red")
                self.ui.status_register.setText(f"{reg.result.success}, reason: {reg.result.reason}")

    def request_control(self):
        self.ui.status_request_control.setText("")
        self.ui.status_release_control.setText("")
        status = self.Access.HostControl.get_state()
        if status.result.success and status.value.canRequestControl:
            control = self.Access.HostControl.request_host_control()
            if control.result.success:
                self.ui.status_request_control.setStyleSheet("color: green")
                self.ui.status_request_control.setText(f"{control.result.success}")
                self.ui.button_release_control.setEnabled(True)
            else:
                self.ui.status_request_control.setStyleSheet("color: red")
                self.ui.status_request_control.setText(f"{control}")
        else:
            self.ui.status_request_control.setStyleSheet("color: red")
            self.ui.status_request_control.setText(f"{status}")

    def release_control(self):
        self.ui.status_request_control.setText("")
        self.ui.status_release_control.setText("")
        status = self.Access.HostControl.get_state()
        if status.result.success and status.value.canReleaseControl:
            control = self.Access.HostControl.release_host_control()
            if control.result.success:
                self.ui.status_release_control.setStyleSheet("color: green")
                self.ui.status_release_control.setText(f"{control.result.success}")
            else:
                self.ui.status_release_control.setStyleSheet("color: red")
                self.ui.status_release_control.setText(f"{control}")

    def get_templates(self):
        templates = self.Access.TemplateExecution.get_templates()
        if templates.result.success:
            for row, template in enumerate(templates.value):
                if row >= self.ui.table_templates.rowCount():
                    self.ui.table_templates.insertRow(row)
                self.ui.table_templates.setItem(row, 0, QTableWidgetItem(template.label))
                self.ui.table_templates.setItem(row, 1, QTableWidgetItem(str(template.isInteractive)))
                self.ui.table_templates.setItem(row, 2, QTableWidgetItem(template.id))
        self.ui.button_open_template.setEnabled(True)

    def open_template(self):
        template = self.ui.table_templates.selectedItems()
        if template:
            self.template_id = template[2].text()
            open_template = self.Access.TemplateModification.open(self.template_id)
            if open_template.result.success:
                self.ui.status_open_template.setStyleSheet("color: green")
                self.ui.status_open_template.setText(f"{open_template.result.success}: {template[0].text()}")
                self.ui.button_start_template.setEnabled(True)
                self.ui.button_stop_template.setEnabled(True)
            else:
                self.ui.status_open_template.setStyleSheet("color: red")
                self.ui.status_open_template.setText(f"{open_template}")

    def start_template(self):
        if self.template_id:
            try:
                start = self.Access.TemplateExecution.start(self.template_id)
                if start.result.success:
                    self.ui.status_start_stop_template.setStyleSheet("color: green")
                    self.ui.status_start_stop_template.setText(f"Start: {start.result.success}")
                else:
                    self.ui.status_start_stop_template.setStyleSheet("color: red")
                    self.ui.status_start_stop_template.setText(f"Start: {start}")
            except Exception as err:
                self.ui.status_start_stop_template.setStyleSheet("color: red")
                self.ui.status_start_stop_template.setText(f"Error: {err}")

    def stop_template(self):
        stop = self.Access.TemplateExecution.stop()
        if self.Access.TemplateExecution.get_state().value.canStop:
            if stop.result.success:
                self.ui.status_start_stop_template.setStyleSheet("color: green")
                self.ui.status_start_stop_template.setText(f"Stop: {stop.result.success}")
            else:
                self.ui.status_start_stop_template.setStyleSheet("color: red")
                self.ui.status_start_stop_template.setText(f"Stop: {stop}")
        self.Access.TemplateModification.close()

    def get_parameter(self):
        parameter = self.ui.combo_get_parameter_choice.currentText()
        try:
            answer = getattr(self.Access.ParameterStandard, parameter)()
            self.Access.ParameterStandard.get_slice_position_dcs()
            if answer.result.success:
                del answer.result
                value = ""
                for attr_name, attr_value in answer.__dict__.items():
                    value += f"{attr_name}: {getattr(answer, attr_name)}\n"
                self.ui.status_get_parameter.setText(f"{value}")
            else:
                self.ui.status_get_parameter.setText(f"{answer.result.reason}")
        except Exception as err:
            self.ui.status_get_parameter.setText(f"Error: {err}")

    def set_parameter(self):
        parameter = self.ui.combo_set_parameter_choice.currentText()
        try:
            val = [float(num.strip()) for num in self.ui.field_parameter_value.text().split(",")]
            if len(val) >= 9:
                val_tuples = [(val[i], val[i + 1], val[i + 2]) for i in range(0, 9, 3)]
                answer = getattr(self.Access.ParameterStandard, parameter)(*val_tuples)
            else:
                answer = getattr(self.Access.ParameterStandard, parameter)(*val)
            if answer.result.success:
                self.ui.status_set_parameter.setText(f"valueSet: {answer.valueSet}")
            else:
                self.ui.status_set_parameter.setText(f"{answer.result.reason}")
        except Exception as err:
            self.ui.status_set_parameter.setText(f"Error: {err}")
