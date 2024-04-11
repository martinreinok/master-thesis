import can


class CustomCanListener(can.Listener):
    def on_message_received(self, msg):
        if msg.arbitration_id == 0x500:  # Check for ID 0x500
            grip_status = bool(msg.data[0])
            guidewire_button = bool(msg.data[1])
            catheter_button = bool(msg.data[2])
            rotary_motor_position = msg.data[3]
            rotary_motor_conversion = msg.data[4]
            linear_motor_position = msg.data[5]
            linear_motor_conversion = msg.data[6]
            # reserved = msg.data[7]

            # print("Received CAN message:")
            # print("Grip Status:", grip_status)
            # print("Guidewire Button:", guidewire_button)
            print("Catheter Button:", catheter_button)
            # print("Rotary Motor Position:", rotary_motor_position)
            # print("Rotary Motor Conversion:", rotary_motor_conversion)
            # print("Linear Motor Position:", linear_motor_position)
            # print("Linear Motor Conversion:", linear_motor_conversion)


# Create a CAN bus instance
bus = can.Bus(interface='ixxat', channel=0, bitrate=1000000)

# Add the custom listener
listener = CustomCanListener()

# Start the listener
notifier = can.Notifier(bus, [listener])
bus.flush_tx_buffer()  # flush any messages that might have built up. (Python is slow)

try:
    while True:
        pass
except KeyboardInterrupt:
    notifier.stop()
