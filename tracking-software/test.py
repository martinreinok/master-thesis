import numpy as np


class MRIProcessor:
    @staticmethod
    def euler_to_rotation_matrix(angles=(0, 0, 0)):
        phi, theta, psi = np.radians(angles)
        R_x = np.array([[1, 0, 0],
                        [0, np.cos(phi), -np.sin(phi)],
                        [0, np.sin(phi), np.cos(phi)]])
        R_y = np.array([[np.cos(theta), 0, np.sin(theta)],
                        [0, 1, 0],
                        [-np.sin(theta), 0, np.cos(theta)]])
        R_z = np.array([[np.cos(psi), -np.sin(psi), 0],
                        [np.sin(psi), np.cos(psi), 0],
                        [0, 0, 1]])
        return np.dot(R_z, np.dot(R_y, R_x))

    @staticmethod
    def get_slice_orientation_degrees_dcs(normal, phase, read):
        rotation_matrix = np.array([normal, phase, read])

        # Calculate Euler angles
        theta = np.arcsin(-rotation_matrix[0, 2])  # pitch
        psi = np.arctan2(rotation_matrix[0, 1], rotation_matrix[0, 0])  # yaw
        phi = np.arctan2(rotation_matrix[1, 2], rotation_matrix[2, 2])  # roll

        # Convert radians to degrees
        normal_deg = np.degrees(phi)
        phase_deg = np.degrees(theta)
        read_deg = np.degrees(psi)

        return normal_deg, phase_deg, read_deg


# Test cases
normal1 = np.array([0, -1, 0])
phase1 = np.array([1, 0, 0])
read1 = np.array([0, 0, 1])
print(MRIProcessor.get_slice_orientation_degrees_dcs(normal1, phase1, read1))  # Output: (0.0, 0.0, 0.0)

normal2 = np.array([0, 0.5735764364, -0.8191520443])
phase2 = np.array([0, -0.8191520443, -0.5735764364])
read2 = np.array([-1, 0, 0])
print(MRIProcessor.get_slice_orientation_degrees_dcs(normal2, phase2, read2))  # Output: (0.0, 55.00000000000001, 0.0)

normal3 = np.array([0, 0, -1])
phase3 = np.array([0, -1, 0])
read3 = np.array([-1, 0, 0])
print(MRIProcessor.get_slice_orientation_degrees_dcs(normal3, phase3, read3))  # Output: (0.0, 90.0, 0.0)

normal4 = np.array([0, -1, 0])
phase4 = np.array([1, 0, 0])
read4 = np.array([0, 0, 1])
print(MRIProcessor.get_slice_orientation_degrees_dcs(normal4, phase4, read4))  # Output: (0.0, 180.0, 0.0)

normal5 = np.array([0, 0, -1])
phase5 = np.array([0, -1, 0])
read5 = np.array([-1, 0, 0])
print(MRIProcessor.get_slice_orientation_degrees_dcs(normal5, phase5, read5))  # Output: (0.0, 270.0, 0.0)

normal6 = np.array([0, -0.7071067812, -0.7071067812])
phase6 = np.array([0, -0.7071067812, 0.7071067812])
read6 = np.array([-1, 0, 0])
print(MRIProcessor.get_slice_orientation_degrees_dcs(normal6, phase6, read6))  # Output: (0.0, 315.0, 0.0)
