import sys
import can
import time
from ui_interface import Ui_MainWindow
from PySide6.QtWidgets import QApplication, QMainWindow, QSlider, QLineEdit


class CathbotInterface(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.pushButton.clicked.connect(self.send_master_canbus_message)
        self.ui.slider_default_resistance.valueChanged.connect(
            lambda: self.change_field_value_from_slider(self.ui.slider_default_resistance,
                                                        self.ui.field_default_resistance))
        self.ui.slider_collision_resistance.valueChanged.connect(
            lambda: self.change_field_value_from_slider(self.ui.slider_collision_resistance,
                                                        self.ui.field_collision_resistance))
        self.ui.slider_linear_translation.valueChanged.connect(
            lambda: self.change_field_value_from_slider(self.ui.slider_linear_translation,
                                                        self.ui.field_linear_translation))
        self.ui.slider_rotary_translation.valueChanged.connect(
            lambda: self.change_field_value_from_slider(self.ui.slider_rotary_translation,
                                                        self.ui.field_rotary_translation))

        self.ui.button_catheter_clamp_forward.clicked.connect(self.move_catheter_clamp_forward)
        self.ui.button_catheter_clamp_backward.clicked.connect(self.move_catheter_clamp_backward)
        self.ui.button_catheter_rotate_forward.clicked.connect(self.move_catheter_rotate_forward)
        self.ui.button_catheter_rotate_backward.clicked.connect(self.move_catheter_rotate_backward)

        self.ui.button_guidewire_clamp_forward.clicked.connect(self.move_guidewire_clamp_forward)
        self.ui.button_guidewire_clamp_backward.clicked.connect(self.move_guidewire_clamp_backward)
        self.ui.button_guidewire_rotate_forward.clicked.connect(self.move_guidewire_rotate_forward)
        self.ui.button_guidewire_rotate_backward.clicked.connect(self.move_guidewire_rotate_backward)

        self.ui.check_clamp_catheter.stateChanged.connect(
            lambda state: self.send_switch_catheter_clamp(self.ui.check_clamp_catheter))
        self.ui.check_clamp_guidewire.stateChanged.connect(
            lambda state: self.send_switch_guidewire_clamp(self.ui.check_clamp_guidewire))

        # Call the function to update default values
        self.change_field_value_from_slider(self.ui.slider_default_resistance, self.ui.field_default_resistance)
        self.change_field_value_from_slider(self.ui.slider_collision_resistance, self.ui.field_collision_resistance)
        self.change_field_value_from_slider(self.ui.slider_linear_translation, self.ui.field_linear_translation)
        self.change_field_value_from_slider(self.ui.slider_rotary_translation, self.ui.field_rotary_translation)

    @staticmethod
    def change_field_value_from_slider(slider: QSlider, field: QLineEdit):
        field.setText(str(slider.value()))

    def move_catheter_clamp_forward(self):
        self.send_slave_canbus_message(0x041, True)

    def move_catheter_clamp_backward(self):
        self.send_slave_canbus_message(0x041, False)

    def move_catheter_rotate_forward(self):
        self.send_slave_canbus_message(0x042, True)

    def move_catheter_rotate_backward(self):
        self.send_slave_canbus_message(0x042, False)

    def move_guidewire_clamp_forward(self):
        self.send_slave_canbus_message(0x043, True)

    def move_guidewire_clamp_backward(self):
        self.send_slave_canbus_message(0x043, False)

    def move_guidewire_rotate_forward(self):
        self.send_slave_canbus_message(0x044, True)

    def move_guidewire_rotate_backward(self):
        self.send_slave_canbus_message(0x044, False)

    def send_switch_catheter_clamp(self, checkbox_object):
        with can.Bus(interface='ixxat', channel=0, bitrate=1000000) as bus:
            message = can.Message(arbitration_id=0x045, data=bytes(
                [0xFF if checkbox_object.isChecked() else 0x00]), is_extended_id=False)
            try:
                bus.send(message)
                time.sleep(0.2)
            except can.CanError:
                print("Message NOT sent")

    def send_switch_guidewire_clamp(self, checkbox_object):
        with can.Bus(interface='ixxat', channel=0, bitrate=1000000) as bus:
            message = can.Message(arbitration_id=0x046, data=bytes(
                [0xFF if checkbox_object.isChecked() else 0x00]), is_extended_id=False)
            try:
                bus.send(message)
                time.sleep(0.2)
            except can.CanError:
                print("Message NOT sent")

    def send_slave_canbus_message(self, can_id, data):
        with can.Bus(interface='ixxat', channel=0, bitrate=1000000) as bus:
            message = can.Message(arbitration_id=can_id, data=bytes(
                [0xFF if data else 0x00]), is_extended_id=False)
            try:
                bus.send(message)
                time.sleep(0.2)
            except can.CanError:
                print("Message NOT sent")

    def send_master_canbus_message(self):
        with can.Bus(interface='ixxat', channel=0, bitrate=1000000) as bus:
            default_continuous_current = self.ui.slider_default_resistance.value()
            default_peak_current = int(default_continuous_current * 1.2)
            collision_continuous_current = self.ui.slider_collision_resistance.value()
            collision_peak_current = int(collision_continuous_current * 1.2)

            linear_translation = self.ui.slider_linear_translation.value()
            rotary_translation = self.ui.slider_rotary_translation.value()

            collision_simulation = self.ui.check_simulate_collision.isChecked()

            simulate_collision_msg = can.Message(arbitration_id=0x190, data=bytes(
                [0xFF if collision_simulation else 0x00]), is_extended_id=False)

            default_current_msg = can.Message(arbitration_id=0x191, data=bytes(
                [default_continuous_current & 0xFF, (default_continuous_current >> 8) & 0xFF,
                 (default_continuous_current >> 16) & 0xFF, (default_continuous_current >> 24) & 0xFF,
                 default_peak_current & 0xFF, (default_peak_current >> 8) & 0xFF,
                 (default_peak_current >> 16) & 0xFF, (default_peak_current >> 24) & 0xFF]), is_extended_id=False)

            collision_current_msg = can.Message(arbitration_id=0x192, data=bytes(
                [collision_continuous_current & 0xFF, (collision_continuous_current >> 8) & 0xFF,
                 (collision_continuous_current >> 16) & 0xFF, (collision_continuous_current >> 24) & 0xFF,
                 collision_peak_current & 0xFF, (collision_peak_current >> 8) & 0xFF,
                 (collision_peak_current >> 16) & 0xFF, (collision_peak_current >> 24) & 0xFF]), is_extended_id=False)

            linear_translation_msg = can.Message(arbitration_id=0x193, data=bytes(
                [linear_translation & 0xFF, (linear_translation >> 8) & 0xFF,
                 (linear_translation >> 16) & 0xFF, (linear_translation >> 24) & 0xFF]), is_extended_id=False)

            rotary_translation_msg = can.Message(arbitration_id=0x194, data=bytes(
                [rotary_translation & 0xFF, (rotary_translation >> 8) & 0xFF,
                 (rotary_translation >> 16) & 0xFF, (rotary_translation >> 24) & 0xFF]), is_extended_id=False)

            try:
                for message in [default_current_msg, collision_current_msg, linear_translation_msg,
                                rotary_translation_msg, simulate_collision_msg]:
                    bus.send(message)
                    time.sleep(0.2)
            except can.CanError:
                print("Message NOT sent")

    @staticmethod
    def start():
        app = QApplication(sys.argv)
        window = CathbotInterface()
        window.show()
        sys.exit(app.exec())


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CathbotInterface()
    window.show()
    sys.exit(app.exec())
