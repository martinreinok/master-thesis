"""
Implementation based on:
"Passive Tracking Exploiting Local Signal Conservation: The White Marker Phenomenon"
"""

import matplotlib.pyplot as plt
import numpy as np

b0 = 1.5  # Tesla
slice_thickness = 10  # mm
TE = 2.85 * 0.001  # seconds
delta_x_V = 5 * 0.0001  # in mm^3
gyromagnetic_ratio = 42576000  # in Hz/T
meshgrid_resolution = 40

# Spatial range for the simulation (in mm)
x = np.linspace(-slice_thickness/2, slice_thickness/2, meshgrid_resolution)
y = np.linspace(-slice_thickness/2, slice_thickness/2, meshgrid_resolution)
z = np.linspace(-slice_thickness/2, slice_thickness/2, meshgrid_resolution)
X, Y, Z = np.meshgrid(x, y, z)

"""
Dipole Field Distortion
"""
c = b0 * delta_x_V / (4 * np.pi)
Bz = c * (X**2 + Y**2 - 2*Z**2) / ((X**2 + Y**2 + Z**2)**(5/2))

# Assuming uniform signal producing spin density, p(x,y,z) can be taken as 1
p_xyz = 1

"""
Dephasing, integration over slice direction
"""
S_axial = 1/slice_thickness * np.trapz(p_xyz * np.exp(-1j * gyromagnetic_ratio * Bz * TE), X, axis=2)
S_coronal = 1/slice_thickness * np.trapz(p_xyz * np.exp(-1j * gyromagnetic_ratio * Bz * TE), Y, axis=0)
S_coronal = np.rot90(S_coronal)

# real and imaginary parts of the signal
S_coronal_real = np.real(S_coronal)
S_coronal_imag = np.imag(S_coronal)
S_axial_real = np.real(S_axial)

"""
Masking signal
"""
threshold = 0.95
mask = np.abs(S_coronal_real) < threshold
masked_signal = np.where(mask, S_coronal_real, np.nan)


plt.figure(figsize=(18, 5))

plt.subplot(1, 3, 1)
plt.imshow(S_coronal_real, extent=(x.min(), x.max(), y.min(), y.max()), cmap="gray")
plt.title("Real Part")
plt.xlabel("x")
plt.ylabel("y")
plt.colorbar()

plt.subplot(1, 3, 2)
plt.imshow(mask, extent=(x.min(), x.max(), y.min(), y.max()), cmap="gray")
plt.title("Mask")
plt.xlabel("x")
plt.ylabel("y")

plt.subplot(1, 3, 3)
plt.imshow(masked_signal, extent=(x.min(), x.max(), y.min(), y.max()), cmap="gray")
plt.title("Masked Real")
plt.xlabel("x")
plt.ylabel("y")

plt.tight_layout()
plt.show()
