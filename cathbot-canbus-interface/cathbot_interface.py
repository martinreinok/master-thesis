import sys
import can
from ui_interface import Ui_MainWindow
from PySide6.QtWidgets import QApplication, QMainWindow, QSlider, QLineEdit


class MyMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.pushButton.clicked.connect(self.send_canbus_message)
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

        # Call the functino to update default values
        self.change_field_value_from_slider(self.ui.slider_default_resistance, self.ui.field_default_resistance)
        self.change_field_value_from_slider(self.ui.slider_collision_resistance, self.ui.field_collision_resistance)
        self.change_field_value_from_slider(self.ui.slider_linear_translation, self.ui.field_linear_translation)
        self.change_field_value_from_slider(self.ui.slider_rotary_translation, self.ui.field_rotary_translation)

    @staticmethod
    def change_field_value_from_slider(slider: QSlider, field: QLineEdit):
        field.setText(str(slider.value()))

    def send_canbus_message(self):
        with can.Bus(interface='ixxat', channel=0, bitrate=1000000) as bus:
            default_continuous_current = self.ui.slider_default_resistance.value()
            default_peak_current = default_continuous_current * 1.2
            collision_continuous_current = self.ui.slider_collision_resistance.value()
            collision_peak_current = collision_continuous_current * 1.2

            linear_translation = self.ui.slider_linear_translation.value()
            rotary_translation = self.ui.slider_rotary_translation.value()

            collision_simulation = self.ui.check_simulate_collision.isChecked()

            simulate_collision_msg = can.Message(arbitration_id=0x190, data=bytes(
                [rotary_translation & 0xFF]), is_extended_id=False)

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
                bus.send(default_current_msg)
                bus.send(collision_current_msg)
                bus.send(linear_translation_msg)
                bus.send(rotary_translation_msg)
                bus.send(simulate_collision_msg)
            except can.CanError:
                print("Message NOT sent")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyMainWindow()
    window.show()
    sys.exit(app.exec())
