#!/usr/bin/env python

"""
This example shows how sending a single message works.
Spacebar: increase current
any key: send message
"""
import time
import keyboard  # Import the keyboard library
import can

current_index = 0


def send_one(can_id, current_continuous, current_peak):
    """Sends a single message."""

    with can.Bus(interface='ixxat', channel=0, bitrate=1000000) as bus:

        msg = can.Message(
            arbitration_id=can_id, data=bytes([current_continuous & 0xFF, (current_continuous >> 8) & 0xFF,
                                               (current_continuous >> 16) & 0xFF, (current_continuous >> 24) & 0xFF,
                                               current_peak & 0xFF, (current_peak >> 8) & 0xFF,
                                               (current_peak >> 16) & 0xFF, (current_peak >> 24) & 0xFF
                                               ]),
            is_extended_id=False)

        try:
            bus.send(msg)
        except can.CanError:
            print("Message NOT sent")


def on_space(event):
    global current_index
    current_index += 1
    current_index %= len(currents)


keyboard.on_press_key("space", on_space)

can_id = 0x997

currents = [current * 10 for current in range(1, 30)]

while True:
    current = currents[current_index]
    print(current)
    send_one(can_id=can_id, current_continuous=int(current), current_peak=int(current * 1.2))
    input()
