import numpy as np

# Define the default vectors
default_normal = np.array([0, -1, 0])
default_phase = np.array([1, 0, 0])
default_read = np.array([0, 0, 1])

normal1 = np.array([0, -1, 0])
phase1 = np.array([1, 0, 0])
read1 = np.array([0, 0, 1])

normal2 = np.array([0, 0, -0.8191520443])
phase2 = np.array([0, -0.8191520443, -0.5735764364])
read2 = np.array([-1, 0, 0])

normal3 = np.array([0, 0, -1])
phase3 = np.array([0, -1, 0])
read3 = np.array([-1, 0, 0])

normal5 = np.array([0, 0, -1])
phase5 = np.array([0, -1, 0])
read5 = np.array([-1, 0, 0])

normal_angle1 = np.arccos(np.dot(normal1, default_normal))
phase_angle1 = np.arccos(np.dot(phase1, default_phase))
read_angle1 = np.arccos(np.dot(read1, default_read))

normal_angle2 = np.arccos(np.dot(normal2, default_normal))
phase_angle2 = np.arccos(np.dot(phase2, default_phase))
read_angle2 = np.arccos(np.dot(read2, default_read))

normal_angle3 = np.arccos(np.dot(normal3, default_normal))
phase_angle3 = np.arccos(np.dot(phase3, default_phase))
read_angle3 = np.arccos(np.dot(read3, default_read))


print(f""
      f"Normal: {90 - np.degrees(normal_angle1) + 90}, "
      f"Phase: {90 - np.degrees(phase_angle1) + 90}, "
      f"Read: {90 - np.degrees(read_angle1) + 90}")

print(f""
      f"Normal: {90 - np.degrees(normal_angle2) + 90}, "
      f"Phase: {90 - np.degrees(phase_angle2) + 90}, "
      f"Read: {90 - np.degrees(read_angle2) + 90}")

print(f""
      f"Normal: {90 - np.degrees(normal_angle3) + 90}, "
      f"Phase: {90 - np.degrees(phase_angle3) + 90}, "
      f"Read: {90 - np.degrees(read_angle3) + 90}")
