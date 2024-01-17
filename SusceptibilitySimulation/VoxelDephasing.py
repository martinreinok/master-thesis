"""
Implementation based on:
"Passive Tracking Exploiting Local Signal Conservation: The White Marker Phenomenon"
"""

import matplotlib.pyplot as plt
import numpy as np


def normalize(array):
    min_val = np.min(array)
    max_val = np.max(array)
    normalized_array = (array - min_val) / (max_val - min_val)
    return normalized_array


"""
Changeable variables
"""
image_resolution = 288  # pixels (square ratio)
voxel_size = 1.2152777910233  # mm
slice_thickness = 8  # mm
echo_time_ms = 4000.45  # ms
b0 = 1.5  # Tesla

"""
Not changeable variables
"""
TE = echo_time_ms * 0.001  # seconds
delta_x_V = voxel_size * 0.001  # Voxel size in m
gyromagnetic_ratio = 425763847  # in Hz/T

image_size = int(image_resolution * voxel_size / 2)
# Spatial range for the simulation (in mm)
x = np.linspace(-image_size, image_size, image_resolution)
y = np.linspace(-image_size, image_size, image_resolution)
z = np.linspace(-image_size, image_size, image_resolution)
X, Y, Z = np.meshgrid(x, y, z)

"""
Dipole Field Distortion
"""
c = b0 * delta_x_V / (4 * np.pi)
Bz = c * (X ** 2 + Y ** 2 - 2 * Z ** 2) / ((X ** 2 + Y ** 2 + Z ** 2) ** (5 / 2))

# Assuming uniform signal producing spin density, p(x,y,z) can be taken as 1
p_xyz = 1

"""
Dephasing, integration over slice direction
"""
S_axial = 1 / slice_thickness * np.trapz(p_xyz * np.exp(-1j * gyromagnetic_ratio * Bz * TE), Z, axis=2)
S_coronal = 1 / slice_thickness * np.trapz(p_xyz * np.exp(-1j * gyromagnetic_ratio * Bz * TE), Y, axis=0)
S_coronal = np.rot90(S_coronal)

# real and imaginary parts of the signal
S_coronal_real = np.real(S_coronal)
S_coronal_imag = np.imag(S_coronal)
S_axial_real = np.real(S_axial)
S_axial_imag = np.imag(S_axial)

# Normalize
S_coronal_real = normalize(S_coronal_real)
S_coronal_imag = normalize(S_coronal_imag)
S_axial_real = normalize(S_axial_real)
S_axial_imag = normalize(S_axial_imag)

"""
Masking signal
"""
threshold = 0.95
mask = np.abs(S_coronal_real) < threshold
masked_signal = np.where(mask, S_coronal_real, np.nan)

# plt.figure(figsize=(image_resolution / 100, image_resolution / 100))

plt.figure(figsize=(18, 12))

plt.subplot(2, 3, 1)
plt.imshow(S_coronal_real, extent=(x.min(), x.max(), y.min(), y.max()), cmap="gray")
plt.title("Real part")
plt.xlabel("x (mm)")
plt.ylabel("y (mm)")
plt.colorbar()

plt.subplot(2, 3, 2)
plt.imshow(S_coronal_imag, extent=(x.min(), x.max(), y.min(), y.max()), cmap="hsv")
plt.title("Phase/Imaginary HSV")
plt.xlabel("x")
plt.ylabel("y")
plt.colorbar()

plt.subplot(2, 3, 3)
plt.imshow(mask, extent=(x.min(), x.max(), y.min(), y.max()), cmap="gray")
plt.title("Mask (for CNN)")
plt.xlabel("x")
plt.ylabel("y")

plt.subplot(2, 3, 4)
plt.imshow(S_coronal_imag, extent=(x.min(), x.max(), y.min(), y.max()), cmap="gray")
plt.title("Phase/Imaginary gray")
plt.xlabel("x")
plt.ylabel("y")
plt.colorbar()

plt.subplot(2, 3, 5)
plt.imshow(S_axial_real, extent=(x.min(), x.max(), y.min(), y.max()), cmap="gray")
plt.title("Axial Real")
plt.xlabel("x")
plt.ylabel("y")
plt.colorbar()

plt.subplot(2, 3, 6)
plt.imshow(S_axial_imag, extent=(x.min(), x.max(), y.min(), y.max()), cmap="gray")
plt.title("Axial Imaginary")
plt.xlabel("x")
plt.ylabel("y")
plt.colorbar()

plt.tight_layout()

plt.show()
