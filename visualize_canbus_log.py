import matplotlib.pyplot as plt
from datetime import datetime

# Open the log file
with open("canbus_log/log13.05.2024_test", "r") as log_file:
    # Parse log file and extract relevant data
    timestamps = []
    rotary_positions = []
    linear_positions = []

    for line in log_file:
        if "ID: 500" in line:
            parts = line.split()
            # Adjust the timestamp format to match the actual format in the log file
            timestamp_str = parts[0][1:] + ' ' + parts[1][:12]
            timestamp = datetime.strptime(timestamp_str, "%Y-%m-%d %H:%M:%S.%f")
            timestamps.append(timestamp)
            data = parts[4:]
            rotary_motor_position = int(data[4], 16)
            linear_motor_position = int(data[6], 16)
            rotary_positions.append(rotary_motor_position)
            linear_positions.append(linear_motor_position)

# Plotting
plt.figure(figsize=(10, 6))
plt.plot(timestamps, rotary_positions, label='Rotary Motor Position', linewidth=2)
plt.plot(timestamps, linear_positions, label='Linear Motor Position', linewidth=2)
plt.xlabel('Time')
plt.ylabel('Position')
plt.title('Motor Positions over Time')
plt.legend()
plt.grid(True)

# Set x-axis limits to show entire timeline
plt.xlim(timestamps[0], timestamps[-1])

plt.show()
